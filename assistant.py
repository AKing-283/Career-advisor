# assistant.py
import os
import time
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv
from career_paths import CAREER_PATHS
from prompts import (
    EXTRACT_INTERESTS_PROMPT,
    MAP_CAREERS_PROMPT,
    EXPLANATION_PROMPT,
    CLARIFYING_QUESTION_PROMPT,
    FALLBACK_PROMPT,
    INITIAL_RESPONSE_PROMPT,
    HANDLE_GENERAL_KNOWLEDGE_PROMPT,
    HANDLE_PERSONAL_QUESTION_PROMPT,
    HANDLE_OFF_TOPIC_PROMPT
)
import requests
import re

load_dotenv()

class CareerAssistant:
    def __init__(self, together_api_key: str = None, max_retries: int = 3):
        self.max_retries = max_retries
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.api_key = together_api_key or os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise ValueError("TOGETHER_API_KEY not found in environment variables")
        self.chat_history = []
        self._initialize_together()

    def _initialize_together(self):
        try:
            response = self._invoke("Hello")
            if not response:
                raise RuntimeError("Failed to get response from Together.ai")
            print("Successfully initialized Together.ai Mistral model")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Together.ai: {str(e)}")

    def _invoke(self, prompt: str, max_tokens: int = 1000) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "max_tokens": max_tokens,
                        "top_p": 0.9,
                        "top_k": 40
                    },
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                if not result or "choices" not in result or not result["choices"]:
                    raise ValueError("Empty or invalid response from Together.ai")
                return result["choices"][0]["message"]["content"].strip()
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                else:
                    return "Error: Could not process request"

    def extract_interests(self, user_input: str) -> List[str]:
        try:
            # Include chat history context
            context = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" for msg in self.chat_history[-3:]])
            prompt = f"{context}\n\nUser: {user_input}\n\n" + EXTRACT_INTERESTS_PROMPT.format(user_input=user_input)
            
            response = self._invoke(prompt)
            try:
                interests = json.loads(response)
                if isinstance(interests, list):
                    return interests[:3]
                elif isinstance(interests, dict) and "interests" in interests:
                    return interests["interests"][:3]
            except json.JSONDecodeError:
                pass
            
            interests = [i.strip() for i in response.split(",") if i.strip()][:3]
            if interests:
                return interests
            
            if "interest" in response.lower() or "enjoy" in response.lower():
                for sep in [".", ":", "-", "\n"]:
                    parts = response.split(sep)
                    interests = [p.strip() for p in parts if any(word in p.lower() for word in ["interest", "enjoy", "like", "love"])][:3]
                    if interests:
                        return interests
            
            return []
        except Exception as e:
            return []

    def map_careers(self, interests: List[str]) -> List[Dict]:
        try:
            matched_careers = []
            interest_keywords = set()
            
            # Extract keywords from interests
            for interest in interests:
                interest_lower = interest.lower()
                # Add the full interest as a keyword
                interest_keywords.add(interest_lower)
                # Add individual words as keywords
                interest_keywords.update(interest_lower.split())
            
            # First pass: exact matches
            for career, details in CAREER_PATHS.items():
                career_keywords = set(k.lower() for k in details.get("keywords", []))
                if interest_keywords.intersection(career_keywords):
                    if career not in [c["title"] for c in matched_careers]:
                        matched_careers.append({
                            "title": career,
                            "description": details.get("description", ""),
                            "category": details.get("category", ""),
                            "skills": details.get("skills", []),
                            "education": details.get("education", ""),
                            "match_score": len(interest_keywords.intersection(career_keywords))
                        })
            
            # If no exact matches, try semantic matching
            if not matched_careers:
                available_careers = list(CAREER_PATHS.keys())
                prompt = MAP_CAREERS_PROMPT.format(
                    interests=", ".join(interests),
                    available_careers=", ".join(available_careers)
                )
                
                response = self._invoke(prompt, max_tokens=1500)
                try:
                    result = json.loads(response)
                    if isinstance(result, dict) and "careers" in result:
                        careers = result["careers"]
                        return [{
                            "title": c["title"],
                            "description": CAREER_PATHS.get(c["title"], {}).get("description", ""),
                            "category": c.get("category", ""),
                            "skills": c.get("required_skills", []),
                            "education": CAREER_PATHS.get(c["title"], {}).get("education", "")
                        } for c in careers[:3] if c["title"] in CAREER_PATHS]
                except json.JSONDecodeError:
                    pass
            
            # Sort by match score and return top 3
            matched_careers.sort(key=lambda x: x["match_score"], reverse=True)
            return matched_careers[:3]
        except Exception as e:
            return []

    def generate_explanation(self, career: Dict) -> str:
        try:
            career_title = career.get("title", "")
            career_description = career.get("description", "")
            category = career.get("category", "")
            skills = ", ".join(career.get("skills", []))
            education = career.get("education", "")
            
            prompt = EXPLANATION_PROMPT.format(
                career_title=career_title,
                career_description=career_description,
                category=category,
                skills=skills,
                education=education
            )
            response = self._invoke(prompt, max_tokens=500)
            if not response:
                return f"This career in {category} requires {education} and skills in {skills}."
            return response
        except Exception as e:
            return "This career could be a good match for you."

    def clarifying_question(self, user_input: str) -> str:
        try:
            # Include chat history for context
            context = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" for msg in self.chat_history[-3:]])
            prompt = f"{context}\n\nUser: {user_input}\n\n" + CLARIFYING_QUESTION_PROMPT.format(user_input=user_input)
            
            response = self._invoke(prompt, max_tokens=300)
            try:
                result = json.loads(response)
                if isinstance(result, dict) and "question" in result:
                    return result["question"]
            except json.JSONDecodeError:
                pass
            
            return response if response else "Could you tell me more about your interests?"
        except Exception as e:
            return "Could you tell me more about your interests?"

    def get_fallback_questions(self) -> List[Dict]:
        try:
            response = self._invoke(FALLBACK_PROMPT, max_tokens=800)
            try:
                questions = json.loads(response)
                if isinstance(questions, list):
                    return questions[:4]
            except json.JSONDecodeError:
                pass
            return []
        except Exception as e:
            return []

    def process(self, user_input: str) -> str:
        try:
            # Add user input to chat history
            self.chat_history.append({"user": user_input, "assistant": ""})
            
            # Check for off-topic questions first
            if self._is_off_topic(user_input):
                response = self._handle_off_topic(user_input)
                self.chat_history[-1]["assistant"] = response
                return response

            # First, try to get an immediate response based on the input
            initial_response = self._invoke(INITIAL_RESPONSE_PROMPT.format(user_input=user_input), max_tokens=1000)
            if initial_response and len(initial_response) > 50:  # If we got a meaningful response
                self.chat_history[-1]["assistant"] = initial_response
                return initial_response

            # If no immediate response, proceed with the normal flow
            interests = self.extract_interests(user_input)
            if not interests:
                fallback_questions = self.get_fallback_questions()
                if fallback_questions:
                    response = "I'd love to help you find the perfect career path! To better understand your interests, could you tell me:\n\n"
                    for q in fallback_questions:
                        response += f"• {q['question']}\n"
                    self.chat_history[-1]["assistant"] = response
                    return response
                response = self.clarifying_question(user_input)
                self.chat_history[-1]["assistant"] = response
                return response

            careers = self.map_careers(interests)
            if not careers:
                response = "I'd love to help you find the right career path. Could you tell me more about what you enjoy doing?"
                self.chat_history[-1]["assistant"] = response
                return response

            # Generate a conversational response
            response = "Based on your interests and preferences, I think these career paths would be perfect for you:\n\n"
            for career in careers:
                career_title = career.get("title", "Unknown Career")
                category = career.get("category", "")
                skills = ", ".join(career.get("skills", []))
                education = career.get("education", "")
                explanation = self.generate_explanation(career)
                
                response += f"• {career_title} ({category}):\n"
                response += f"  {explanation}\n"
                response += f"  Required Education: {education}\n"
                response += f"  Key Skills: {skills}\n\n"

            response += "Would you like to know more about any of these careers? Or would you like to explore other options?"
            self.chat_history[-1]["assistant"] = response
            return response
        except Exception as e:
            response = "I apologize, but I'm having trouble processing that. Could you try rephrasing your interests?"
            self.chat_history[-1]["assistant"] = response
            return response

    def _is_off_topic(self, user_input: str) -> bool:
        input_lower = user_input.lower()
        
        patterns = {
            "current_events": [
                r"war", r"conflict", r"attack", r"bombing", r"invasion",
                r"crisis", r"emergency", r"disaster", r"tragedy",
                r"latest", r"breaking", r"news", r"update", r"developing",
                r"just in", r"recent", r"today", r"yesterday", r"this week"
            ],
            "geopolitical": [
                r"country", r"nation", r"state", r"government", r"politics",
                r"diplomacy", r"foreign", r"international", r"global",
                r"treaty", r"agreement", r"alliance", r"sanction", r"embargo",
                r"border", r"territory", r"region", r"zone", r"area"
            ],
            "sensitive": [
                r"violence", r"crime", r"terror", r"attack", r"threat",
                r"danger", r"risk", r"hazard", r"emergency",
                r"death", r"kill", r"injure", r"hurt", r"damage",
                r"abuse", r"harass", r"discriminate", r"hate", r"prejudice"
            ],
            "weather": [
                r"weather", r"temperature", r"forecast", r"rain", r"sunny", r"cloudy",
                r"humidity", r"wind", r"storm", r"climate", r"season",
                r"natural disaster", r"earthquake", r"flood", r"hurricane", r"tornado"
            ],
            "general_knowledge": [
                r"where is", r"what is", r"how to", r"tell me about", r"explain",
                r"define", r"meaning of", r"location of", r"address of",
                r"capital of", r"population of", r"size of", r"distance to"
            ],
            "time_date": [
                r"time", r"date", r"day", r"month", r"year",
                r"calendar", r"schedule", r"appointment", r"deadline"
            ],
            "sports_entertainment": [
                r"sports", r"scores", r"game", r"match", r"tournament",
                r"player", r"team", r"league", r"championship",
                r"movie", r"film", r"show", r"entertainment",
                r"music", r"concert", r"performance", r"artist"
            ],
            "biographical": [
                r"who was", r"who is", r"biography", r"history", r"famous",
                r"president", r"prime minister", r"leader", r"scientist",
                r"inventor", r"discoverer", r"author", r"writer",
                r"born", r"died", r"lived", r"achieved", r"accomplished"
            ],
            "academic": [
                r"teach", r"learn", r"study", r"education", r"school",
                r"college", r"university", r"course", r"subject",
                r"exam", r"test", r"assignment", r"homework", r"project"
            ],
            "technical": [
                r"how does", r"how do", r"explain how", r"describe how",
                r"what causes", r"why does", r"what makes",
                r"function", r"work", r"operate", r"process"
            ],
            "personal": [
                r"you", r"your", r"yourself", r"your life", r"your background",
                r"your experience", r"your knowledge", r"your opinion",
                r"your thoughts", r"your feelings", r"your preferences"
            ],
            "shopping": [
                r"buy", r"sell", r"price", r"cost", r"shopping",
                r"product", r"item", r"store", r"shop", r"market"
            ],
            "travel": [
                r"travel", r"trip", r"journey", r"destination",
                r"place", r"location", r"city", r"country",
                r"visit", r"tour", r"vacation", r"holiday"
            ],
            "health": [
                r"health", r"medical", r"doctor", r"hospital",
                r"disease", r"illness", r"symptom", r"treatment",
                r"medicine", r"drug", r"vaccine", r"cure"
            ]
        }
        
        return any(re.search(pattern, input_lower) for pattern_list in patterns.values() for pattern in pattern_list)

    def _handle_off_topic(self, user_input: str) -> str:
        input_lower = user_input.lower()
        
        responses = {
            "current_events": "I'm a career guidance assistant, and I notice you're asking about current events. While I can't provide information about that topic, I'm here to help you explore careers and find the right path for you.",
            "geopolitical": "I'm a career guidance assistant, and I notice you're asking about geopolitical matters. While I can't provide information about that topic, I'm here to help you explore careers and find the right path for you.",
            "sensitive": "I'm a career guidance assistant, and I notice you're asking about a sensitive topic. While I can't provide information about that topic, I'm here to help you explore careers and find the right path for you.",
            "weather": "I'm a career guidance assistant, and I notice you're asking about the weather. While I can't provide weather information, I'm here to help you explore careers and find the right path for you.",
            "general_knowledge": "I'm a career guidance assistant, and I notice you're asking about general knowledge. While I can't provide that information, I'm here to help you explore careers and find the right path for you.",
            "biographical": "I'm a career guidance assistant, and I notice you're asking about a person or historical figure. While I can't provide biographical information, I'm here to help you explore careers and find the right path for you.",
            "personal": "I'm a career guidance assistant, and I notice you're asking about me. While I can't share personal information, I'm here to help you explore careers and find the right path for you.",
            "technical": "I'm a career guidance assistant, and I notice you're asking about technical details. While I can't provide that information, I'm here to help you explore careers and find the right path for you.",
            "default": "I'm a career guidance assistant, and I notice your question is outside the scope of career guidance. I'm here to help you explore careers and find the right path for you."
        }
        
        category = "default"
        if any(word in input_lower for word in ["war", "conflict", "attack", "crisis", "news"]):
            category = "current_events"
        elif any(word in input_lower for word in ["country", "nation", "government", "politics"]):
            category = "geopolitical"
        elif any(word in input_lower for word in ["violence", "crime", "terror", "danger"]):
            category = "sensitive"
        elif any(word in input_lower for word in ["weather", "temperature", "forecast"]):
            category = "weather"
        elif any(word in input_lower for word in ["who was", "who is", "biography", "history"]):
            category = "biographical"
        elif any(word in input_lower for word in ["you", "your", "yourself"]):
            category = "personal"
        elif any(word in input_lower for word in ["how does", "how do", "explain how"]):
            category = "technical"
        elif any(word in input_lower for word in ["what is", "where is", "tell me about"]):
            category = "general_knowledge"
            
        response = responses.get(category, responses["default"])
        response += "\n\nWould you like to:\n"
        response += "1. Learn about different career options?\n"
        response += "2. Discover jobs that match your interests?\n"
        response += "3. Understand what skills you need for specific careers?\n"
        response += "4. Get guidance on choosing the right career path?\n\n"
        response += "Just let me know what interests you, and I'll help you find the perfect career match!"
        
        return response 