import streamlit as st
import requests
import json
from datetime import datetime
import os

st.set_page_config(page_title="Vishesh AI Chatbot", page_icon="", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #2d2d2d 0%, #252525 100%);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border: 1px solid #3a3a3a;
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.8em;
        margin: 0;
        font-weight: 600;
    }
    
    .main-header p {
        color: #aaa;
        margin-top: 12px;
        font-size: 1.1em;
    }
    
    .chat-container {
        background: #1f1f1f;
        padding: 30px;
        border-radius: 20px;
        min-height: 150px;
        max-height: 500px;
        overflow-y: auto;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .user-msg {
        background: linear-gradient(135deg, #2d5a9e 0%, #1e4178 100%);
        padding: 18px 24px;
        border-radius: 18px;
        margin: 12px 0;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(45,90,158,0.25);
        animation: slideInRight 0.4s ease-out;
        border-left: 3px solid #4a90e2;
    }
    
    .ai-msg {
        background: linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%);
        padding: 18px 24px;
        border-radius: 18px;
        margin: 12px 0;
        color: #f0f0f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideInLeft 0.4s ease-out;
        border-left: 3px solid #666;
    }
    
    .user-msg strong, .ai-msg strong {
        display: block;
        margin-bottom: 10px;
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    .timestamp {
        font-size: 0.75em;
        opacity: 0.5;
        margin-top: 8px;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1f1f 0%, #1a1a1a 100%);
        border-right: 1px solid #3a3a3a;
    }
    
    section[data-testid="stSidebar"] h1 {
        color: #ffffff;
    }
    
    section[data-testid="stSidebar"] .stMetric {
        background: linear-gradient(135deg, #2d2d2d 0%, #252525 100%);
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        border: 1px solid #3a3a3a;
        transition: all 0.3s ease;
    }
    
    section[data-testid="stSidebar"] .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(74,144,226,0.15);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74,144,226,0.3);
    }
    
    .stButton button:hover {
        background: #4a90e2;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74,144,226,0.4);
    }
    
    .welcome {
        text-align: center;
        padding: 40px 20px;
        color: #999;
    }
    
    .welcome h2 {
        color: #ffffff;
        margin-bottom: 25px;
        font-size: 2.2em;
    }
    
    .welcome p {
        font-size: 1.15em;
        line-height: 1.8;
    }
    
    .footer {
        text-align: center;
        padding: 25px;
        color: #666;
        margin-top: 40px;
        border-top: 1px solid #3a3a3a;
    }
    
    .footer a {
        color: #4a90e2;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .footer a:hover {
        color: #5ba3f5;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4a90e2 0%, #357abd 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1> Vishesh AI Chatbot</h1>
    <p>Powered by Gemini 2.5 Flash  Smart  Fast  Reliable</p>
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
    
    context = "You are an intelligent AI assistant created by Vishesh Sanghvi. You provide helpful, accurate, and friendly responses. Keep conversations natural and engaging.\n\n"
    for msg in messages[-20:]:
        context += f"{msg['role'].title()}: {msg['content']}\n"
    
    payload = {
        "contents": [{"parts": [{"text": context}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 4096}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f" Error {resp.status_code}: Unable to get response"
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
        st.success(" Connected")
    else:
        st.error(" No API Key")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Memory", f"{min(len(st.session_state.messages), 20)}/20")
    
    st.metric("AI Model", "Gemini 2.5 Flash")
    
    st.divider()
    
    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("** Created by:**")
    st.markdown("[Vishesh Sanghvi](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h2> Welcome to Vishesh AI!</h2>
        <p>I'm here to help you with anything you need.</p>
        <p>Ask me questions, request explanations, or just chat!</p>
        <p> I remember our conversation for context-aware responses.</p>
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


