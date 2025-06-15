import streamlit as st
from assistant import CareerAssistant
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize the assistant
assistant = CareerAssistant()

# Set page config
st.set_page_config(
    page_title="Career Path Assistant",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for chatbot-like interface
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #f0f2f6;
    }
    
    
    /* Message bubbles */
    .message {
        margin: 10px 0;
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background-color: #007AFF;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background-color: #f0f2f6;
        color: #1a1a1a;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Career cards */
    .career-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .career-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .career-title {
        color: #007AFF;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .career-category {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 5px;
    }
    
    .career-description {
        color: #333;
        margin-bottom: 10px;
    }
    
    .career-skills {
        color: #666;
        font-size: 0.9em;
    }
    
    /* Input area */
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #007AFF;
        box-shadow: 0 0 0 1px #007AFF;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 16px;
        background-color: #007AFF;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
    }
    
    /* Quick response buttons */
    .quick-response {
        display: inline-block;
        margin: 5px;
        padding: 8px 16px;
        background-color: #f0f2f6;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-response:hover {
        background-color: #007AFF;
        color: white;
    }
    
    /* Typing indicator */
    .typing-indicator {
        color: #666;
        font-style: italic;
        margin: 10px 0;
    }
    
    /* Follow-up section */
    .follow-up {
        background-color: #f8f9fa;
        border-left: 4px solid #007AFF;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_career' not in st.session_state:
    st.session_state.selected_career = None
if 'show_follow_up' not in st.session_state:
    st.session_state.show_follow_up = False
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

# Title and description
st.title("🎯 Career Path Assistant")
st.markdown("""
    <div style='text-align: center; color: #666; margin-bottom: 20px;'>
        Tell me about your interests and I'll help you find the perfect career path!
    </div>
""", unsafe_allow_html=True)

# Create chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Function to extract career titles from response
def extract_career_titles(response):
    titles = []
    if '•' in response:
        parts = response.split('•')
        for part in parts[1:]:
            if '(' in part:
                title = part.split('(')[0].strip()
                titles.append(title)
    return titles

# Function to handle quick response clicks
def handle_quick_response(response):
    st.session_state.chat_history.append({
        'role': 'user',
        'content': response
    })
    with st.spinner("Thinking..."):
        assistant_response = assistant.process(response)
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': assistant_response
        })
    st.session_state.show_follow_up = False
    st.session_state.message_count += 1
    st.experimental_rerun()

# Display chat history
for idx, message in enumerate(st.session_state.chat_history):
    if message['role'] == 'user':
        st.markdown(f"""
            <div class="message user-message">
                {message['content']}
            </div>
        """, unsafe_allow_html=True)
    else:
        # Check if the message contains career suggestions
        if '•' in message['content']:
            parts = message['content'].split('•')
            intro = parts[0]
            st.markdown(f"""
                <div class="message assistant-message">
                    {intro}
                </div>
            """, unsafe_allow_html=True)
            
            # Display each career suggestion as a card
            for career in parts[1:]:
                if career.strip():
                    st.markdown(f"""
                        <div class="career-card">
                            {career.strip()}
                        </div>
                    """, unsafe_allow_html=True)
            
            # Add follow-up section
            st.markdown("""
                <div class="follow-up">
                    <h3>Would you like to:</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Add quick response buttons with unique keys
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Tell me more about these careers", key=f"more_careers_{idx}"):
                    handle_quick_response("Tell me more about these careers")
            with col2:
                if st.button("Explore other options", key=f"explore_options_{idx}"):
                    handle_quick_response("What other career options do you have?")
            
            # Add specific career buttons
            career_titles = extract_career_titles(message['content'])
            if career_titles:
                st.markdown("""
                    <div class="follow-up">
                        <h3>Or learn more about a specific career:</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(len(career_titles))
                for i, title in enumerate(career_titles):
                    with cols[i]:
                        if st.button(f"Learn about {title}", key=f"learn_{title}_{idx}"):
                            handle_quick_response(f"Tell me more about {title}")
        else:
            st.markdown(f"""
                <div class="message assistant-message">
                    {message['content']}
                </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Create a form for input
with st.form(key='chat_form'):
    user_input = st.text_input("What are your interests?", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label='Send')

# Handle form submission
if submit_button and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })
    
    # Get assistant's response
    with st.spinner("Thinking..."):
        response = assistant.process(user_input)
        
        # Add assistant's response to chat history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
    
    st.session_state.message_count += 1
    # Rerun to update the chat history
    st.experimental_rerun()

# Add some space at the bottom
st.markdown("<br>" * 2, unsafe_allow_html=True) 