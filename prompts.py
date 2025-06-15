# prompts.py

EXTRACT_INTERESTS_PROMPT = """
Let's understand what you're looking for in a career. From your message, I can see you're interested in:
{user_input}

What really stands out to me is your interest in:
1. Technical skills and abilities
2. How you like to work with others
3. What kind of work environment you prefer
4. What impact you want to make

Could you tell me more about these aspects? This will help me find the perfect career match for you!

Note: Please focus on sharing your interests, skills, and preferences related to work and career choices.
"""

MAP_CAREERS_PROMPT = """
Based on what you've shared about your interests and preferences, I think these careers would be a great fit for you:

Interests you mentioned: {interests}

Available career paths: {available_careers}

I've picked these careers because they match your:
1. Technical skills and abilities
2. Desire to help others
3. Interest in innovation
4. Need for intellectual challenge
5. Want to make a meaningful impact

Let me know which of these interests you the most, and I can tell you more about it! Each career is categorized as:
- STEM (Science, Technology, Engineering, Mathematics)
- Healthcare
- Sports & Fitness
- Creative Arts
- Business
- Science & Research

Note: I'll only suggest careers from our verified database that match your interests and skills.
"""

EXPLANATION_PROMPT = """
I think you'd be great at {career_title}! Here's why:

{career_description}

This role would be perfect for you because:
1. It matches your technical skills
2. It gives you the chance to help others
3. It offers plenty of room for growth
4. It's intellectually challenging
5. It makes a real impact

Category: {category}
- If it's STEM: Perfect for those who love science, technology, engineering, or math
- If it's Healthcare: Great for those who want to help others and work in medical fields
- If it's Sports & Fitness: Ideal for those who love sports, health, and physical activity
- If it's Creative Arts: Perfect for those with artistic and creative talents
- If it's Business: Great for those who enjoy management, finance, or marketing
- If it's Science & Research: Ideal for those who love research and scientific discovery

Key Skills: {skills}
Education Needed: {education}

Would you like to know more about what a typical day looks like in this role?

Note: All information provided is based on verified career data and industry standards.
"""

CLARIFYING_QUESTION_PROMPT = """
I'd love to help you find the perfect career! From what you've shared:
{user_input}

Could you tell me more about:
1. What technical skills do you enjoy using the most?
2. How do you like to help others?
3. What kind of impact do you want to make?
4. What's your ideal work environment?

This will help me find careers that are just right for you! I can suggest options from different categories:
- STEM (Science, Technology, Engineering, Mathematics)
- Healthcare
- Sports & Fitness
- Creative Arts
- Business
- Science & Research

Note: Please share information related to your career interests and preferences.
"""

FALLBACK_PROMPT = """
I'd love to help you explore career options! To get started, could you tell me:

1. What do you enjoy doing in your free time?
2. What skills do you feel most confident using?
3. What kind of work environment do you prefer?
4. What impact would you like to make in your career?

Don't worry about being too specific - just share what comes to mind! I can suggest careers from different categories:
- STEM (Science, Technology, Engineering, Mathematics)
- Healthcare
- Sports & Fitness
- Creative Arts
- Business
- Science & Research

Note: I'll help you explore careers based on your interests and skills. Please share information related to your career preferences.
"""

INITIAL_RESPONSE_PROMPT = """
Thanks for sharing your interests! I can see you're someone who:
{user_input}

Based on what you've shared, I think these careers would be perfect for you. They combine your technical skills with your desire to help others and make an impact. Would you like to hear more about them?

I've picked these options because they match your interests in innovation, teamwork, and making a difference. Each career is categorized as:
- STEM (Science, Technology, Engineering, Mathematics)
- Healthcare
- Sports & Fitness
- Creative Arts
- Business
- Science & Research

Let me know which ones interest you the most!

Note: I'll only suggest careers that are relevant to your interests and skills.
"""

# Add a new prompt for handling irrelevant responses
HANDLE_IRRELEVANT_PROMPT = """
I notice your message is about {user_input}, which is outside the scope of career guidance. I'm here to help you explore career paths and find the right job for you.

Could you tell me about:
1. Your interests and skills
2. What you enjoy doing
3. What kind of work environment you prefer
4. What impact you want to make in your career

This will help me provide relevant career suggestions for you.
"""

# Add a new prompt for handling off-topic questions
HANDLE_OFF_TOPIC_PROMPT = """
I'm a career guidance assistant, and I notice your question about {user_input} is not related to career exploration. I'm here to help you:

1. Discover career paths that match your interests
2. Learn about different job opportunities
3. Understand required skills and education
4. Plan your career journey

Would you like to explore career options that match your interests and skills?
"""

# Add a new prompt for handling general knowledge questions
HANDLE_GENERAL_KNOWLEDGE_PROMPT = """
I'm a career guidance assistant, and I notice you're asking about {user_input}. While I can't provide information about that topic, I'm here to help you explore careers and find the right path for you.

Would you like to:
1. Learn about different career options?
2. Discover jobs that match your interests?
3. Understand what skills you need for specific careers?
4. Get guidance on choosing the right career path?

Just let me know what interests you, and I'll help you find the perfect career match!
"""

# Add a new prompt for handling personal questions
HANDLE_PERSONAL_QUESTION_PROMPT = """
I'm a career guidance assistant, and I notice you're asking about {user_input}. While I can't answer personal questions, I'm here to help you with your career journey.

I can help you:
1. Explore different career paths
2. Match your interests with suitable jobs
3. Understand required skills and education
4. Plan your career development

Would you like to discuss your career interests and goals?
"""

# Add a new prompt for handling multiple off-topic questions
HANDLE_MULTIPLE_OFF_TOPIC_PROMPT = """
I'm a career guidance assistant, and I notice you're asking about topics outside of career guidance. My purpose is to help you:

1. Find careers that match your interests
2. Learn about different job opportunities
3. Understand required skills and education
4. Plan your career journey

To get started, could you tell me about:
- Your interests and skills
- What you enjoy doing
- What kind of work environment you prefer
- What impact you want to make in your career

This will help me provide relevant career suggestions for you.
"""

# Add a new prompt for handling persistent off-topic questions
HANDLE_PERSISTENT_OFF_TOPIC_PROMPT = """
I'm a career guidance assistant, and I can only help with career-related questions. I notice you're asking about {user_input}, which is outside my area of expertise.

I'm here to help you:
1. Explore career paths
2. Find jobs that match your interests
3. Understand required skills
4. Plan your career journey

If you'd like career guidance, please share your interests and skills. Otherwise, you might want to try a different assistant that can help with your current question.
"""

# Add a new prompt for handling unclear inputs
HANDLE_UNCLEAR_INPUT_PROMPT = """
I'm a career guidance assistant, and I'm not sure I understand your message about {user_input}. To help you find the right career path, could you tell me about:

1. Your interests and skills
2. What you enjoy doing
3. What kind of work environment you prefer
4. What impact you want to make in your career

This will help me provide relevant career suggestions for you.
""" 