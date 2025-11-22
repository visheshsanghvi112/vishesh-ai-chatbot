import streamlit as st
import requests
import json
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Vishesh AI Chatbot", page_icon="", layout="wide", initial_sidebar_state="expanded")

# Clean modern dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }
    
    .main-header {
        background: #2d2d2d;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: #00FF00;
        font-size: 2.5em;
        margin: 0;
    }
    
    .main-header p {
        color: #999;
        margin-top: 10px;
    }
    
    .chat-container {
        background: #242424;
        padding: 25px;
        border-radius: 15px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .user-msg {
        background: #333333;
        padding: 15px 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: #00FF00;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .ai-msg {
        background: #444444;
        padding: 15px 20px;
        border-radius: 15px;
        margin: 10px 0;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .user-msg strong, .ai-msg strong {
        display: block;
        margin-bottom: 8px;
        font-size: 1.05em;
    }
    
    .timestamp {
        font-size: 0.8em;
        opacity: 0.6;
        margin-top: 5px;
    }
    
    section[data-testid="stSidebar"] {
        background: #242424;
    }
    
    section[data-testid="stSidebar"] .stMetric {
        background: #2d2d2d;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .stButton button {
        background: #00FF00;
        color: #000000;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #00DD00;
        transform: translateY(-2px);
    }
    
    .welcome {
        text-align: center;
        padding: 80px 20px;
        color: #999;
    }
    
    .welcome h2 {
        color: #00FF00;
        margin-bottom: 20px;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        margin-top: 30px;
    }
    
    .footer a {
        color: #00FF00;
        text-decoration: none;
    }
    
    .footer a:hover {
        color: #00DD00;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00FF00;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1> Vishesh GPT Chatbot</h1>
    <p>AI Assistant powered by Gemini 2.5 Flash</p>
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
    
    context = "You are an intelligent AI assistant created by Vishesh Sanghvi. You remember the conversation and provide helpful, detailed responses.\n\n"
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

with st.sidebar:
    st.title(" Settings")
    
    try:
        has_key = bool(st.secrets.get("GEMINI_API_KEY"))
    except:
        has_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if has_key:
        st.success(" API Key OK")
    else:
        st.error(" No API Key")
    
    st.divider()
    
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Memory", f"{min(len(st.session_state.messages), 20)}/20")
    st.metric("Model", "Gemini 2.5 Flash")
    
    st.divider()
    
    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("**Created by:**")
    st.markdown("[Vishesh Sanghvi](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h2> Welcome!</h2>
        <p>Start chatting by typing a message below.</p>
        <p>I remember our conversation and can help with anything!</p>
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

if prompt := st.chat_input("Type your message here..."):
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

st.markdown("""
<div class="footer">
    <p>Created with  by <a href="https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/" target="_blank">Vishesh Sanghvi</a></p>
    <p>Powered by Google Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)
