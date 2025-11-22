import streamlit as st
import requests
import json
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Vishesh AI Chatbot", page_icon="", layout="wide", initial_sidebar_state="expanded")

# Enhanced CSS with animations and modern design
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        animation: slideDown 0.5s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 10px;
        font-size: 1.1em;
    }
    
    /* Chat message styling */
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
        max-width: 80%;
        margin-left: auto;
    }
    
    .ai-msg {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        animation: slideInLeft 0.3s ease-out;
        max-width: 80%;
    }
    
    .user-msg strong, .ai-msg strong {
        font-size: 1.1em;
        display: block;
        margin-bottom: 8px;
        opacity: 0.9;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-height: 400px;
        margin-bottom: 20px;
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3561 0%, #1f2544 100%);
    }
    
    section[data-testid="stSidebar"] .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.4);
    }
    
    /* Input styling */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 30px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    
    .footer a:hover {
        color: #764ba2;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.8em;
        opacity: 0.7;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1> Vishesh AI Assistant</h1>
    <p>Powered by Gemini 2.5 Flash  Intelligent  Context-Aware</p>
</div>
""", unsafe_allow_html=True)

def get_ai_response(messages):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return " API Key not configured. Add GEMINI_API_KEY to Streamlit secrets."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    context = "You are an intelligent AI assistant created by Vishesh Sanghvi. You remember the conversation and provide helpful, detailed, and friendly responses. Use emojis when appropriate to make conversations engaging.\n\n"
    for msg in messages[-20:]:
        context += f"{msg['role'].title()}: {msg['content']}\n"
    
    payload = {
        "contents": [{"parts": [{"text": context}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 4096}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f" Error {resp.status_code}: {resp.text[:100]}"
    except Exception as e:
        return f" Error: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("###  Control Panel")
    
    try:
        has_key = bool(st.secrets.get("GEMINI_API_KEY"))
    except:
        has_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if has_key:
        st.success(" API Connected")
    else:
        st.error(" No API Key")
    
    st.divider()
    
    st.metric(" Total Messages", len(st.session_state.messages))
    st.metric(" Memory", f"{min(len(st.session_state.messages), 20)}/20")
    st.metric(" Model", "Gemini 2.5")
    
    st.divider()
    
    if st.button(" Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    ###  Tips
    - Ask anything!
    - I remember our conversation
    - Try complex questions
    - Request code, explanations, etc.
    """)
    
    st.divider()
    
    st.markdown("""
    ###  Creator
    **Vishesh Sanghvi**
    
    [ LinkedIn](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)
    """)

# Main chat area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 50px; color: rgba(255,255,255,0.7);">
        <h2> Welcome!</h2>
        <p>Start a conversation by typing a message below.</p>
        <p>I'm here to help with anything you need!</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    css_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    icon = "" if msg["role"] == "user" else ""
    timestamp = msg.get("timestamp", datetime.now()).strftime("%H:%M")
    
    st.markdown(f"""
    <div class="{css_class}">
        <strong>{icon} {msg["role"].title()}</strong>
        <div>{msg["content"]}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input(" Type your message here..."):
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    with st.spinner(" Thinking..."):
        response = get_ai_response(st.session_state.messages)
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now()
    })
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>Created with  by <a href="https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/" target="_blank">Vishesh Sanghvi</a> | Powered by Google Gemini 2.5 Flash</p>
    <p style="font-size: 0.9em; margin-top: 10px;"> Fast   Intelligent   Context-Aware</p>
</div>
""", unsafe_allow_html=True)
