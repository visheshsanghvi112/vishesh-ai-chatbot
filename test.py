import streamlit as st
import requests
import json
from datetime import datetime
import os

st.set_page_config(page_title="Vishesh AI", page_icon="", layout="wide")

# ChatGPT-style CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .stApp {
        background-color: #343541;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        margin-bottom: 0;
        display: flex;
        gap: 1.5rem;
    }
    
    .chat-message.user {
        background-color: #343541;
    }
    
    .chat-message.assistant {
        background-color: #444654;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    
    .chat-message.user .avatar {
        background-color: #5436DA;
    }
    
    .chat-message.assistant .avatar {
        background-color: #19C37D;
    }
    
    .chat-message .message {
        color: #ECECF1;
        font-size: 1rem;
        line-height: 1.7;
        flex: 1;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #202123;
        border-right: 1px solid #4d4d4f;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ECECF1;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #C5C5D2;
    }
    
    /* Buttons */
    .stButton button {
        background-color: transparent;
        border: 1px solid #565869;
        color: #ECECF1;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background-color: #2A2B32;
    }
    
    /* Chat input */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 250px;
        right: 0;
        background: linear-gradient(180deg, transparent, #343541 20%);
        padding: 2rem;
    }
    
    .stChatInput textarea {
        background-color: #40414F;
        border: 1px solid #565869;
        color: #ECECF1;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stChatInput textarea:focus {
        border-color: #19C37D;
        outline: none;
    }
    
    /* Metrics */
    section[data-testid="stSidebar"] .stMetric {
        background-color: #2A2B32;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid #4d4d4f;
    }
    
    section[data-testid="stSidebar"] .stMetric label {
        color: #8E8EA0;
        font-size: 0.875rem;
    }
    
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #ECECF1;
    }
    
    /* Welcome screen */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        color: #ECECF1;
    }
    
    .welcome-screen h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .welcome-screen p {
        color: #8E8EA0;
        font-size: 1.1rem;
    }
    
    /* Divider */
    hr {
        border-color: #4d4d4f;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_ai_response(messages):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return " API Key not configured. Please add GEMINI_API_KEY to Streamlit secrets."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    context = "You are a helpful AI assistant created by Vishesh Sanghvi. Provide clear, accurate, and conversational responses.\n\n"
    for msg in messages[-20:]:
        context += f"{msg['role'].title()}: {msg['content']}\n"
    
    payload = {
        "contents": [{"parts": [{"text": context}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: Unable to get response (Status {resp.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### Vishesh AI")
    
    if st.button(" New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### Status")
    
    try:
        has_key = bool(st.secrets.get("GEMINI_API_KEY"))
    except:
        has_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if has_key:
        st.success("Connected")
    else:
        st.error("No API Key")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Model", "2.5")
    
    st.markdown("---")
    
    st.markdown("### About")
    st.markdown("""
    **Vishesh AI Assistant**
    
    Powered by Google Gemini 2.5 Flash
    
    Created by [Vishesh Sanghvi](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)
    """)

# Main chat area
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-screen">
        <h1> Vishesh AI</h1>
        <p>How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar"></div>
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="avatar"></div>
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Message Vishesh AI..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.spinner(""):
        response = get_ai_response(st.session_state.messages)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()
