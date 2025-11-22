import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from time import sleep
from datetime import datetime
import numpy as np
import base64
import os

# ---- PAGE CONFIGURATION ----
st.set_page_config(
    page_title="AI Milestone - Enhanced GPT Chatbot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
    body { background-color: #000000; color: #ffffff; font-family: 'Courier New', monospace; }
    .header { background-color: #1e1e1e; color: #00FF00; padding: 20px; border-radius: 10px; text-align: center; font-size: 30px; font-weight: bold; box-shadow: 0px 4px 10px rgba(0, 255, 0, 0.4); }
    .chat-container { max-height: 600px; overflow-y: auto; padding: 20px; border-radius: 10px; background-color: #1a1a1a; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); }
    .user-message { background-color: #333333; padding: 15px; border-radius: 8px; margin: 10px 0; color: #00FF00; }
    .assistant-message { background-color: #444444; padding: 15px; border-radius: 8px; margin: 10px 0; color: #ffffff; }
    .timestamp { font-size: 12px; color: #999999; text-align: right; }
    .footer { text-align: center; font-size: 14px; color: #999999; margin-top: 20px; }
    .footer a { color: #00FF00; text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"> AI Milestone - Vishesh GPT Chatbot</div>', unsafe_allow_html=True)

# ---- ENHANCED API WITH MEMORY ----
def get_response_from_api(messages):
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        pass
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return " **API Key Not Configured**\n\nSet GEMINI_API_KEY in:\n- Streamlit Cloud: App Settings  Secrets\n- Local: .streamlit/secrets.toml or environment variable\n\nGet API key: https://makersuite.google.com/app/apikey"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    system_prompt = """You are an intelligent AI assistant similar to ChatGPT, created by Vishesh Sanghvi. You maintain full conversation context, provide detailed responses, and engage naturally. Remember all previous messages."""
    
    conversation_text = system_prompt + "\n\n"
    recent_messages = messages[-30:] if len(messages) > 30 else messages
    
    for msg in recent_messages:
        role = "User" if msg['role'] == 'user' else "Assistant"
        conversation_text += f"{role}: {msg['content']}\n"
    
    data = {
        "contents": [{"parts": [{"text": conversation_text}]}],
        "generationConfig": {"temperature": 0.9, "topK": 40, "topP": 0.95, "maxOutputTokens": 4096}
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        elif response.status_code == 403:
            return " Invalid API key. Get new one at: https://makersuite.google.com/app/apikey"
        elif response.status_code == 429:
            return " Rate limit exceeded. Wait 1-2 minutes."
        else:
            return f" API Error {response.status_code}"
    except Exception as e:
        return f" Error: {str(e)}"

# ---- COMMANDS ----
def handle_commands(user_input):
    cmd = user_input.lower().strip()
    if cmd in ["/help", "help"]:
        return "**Commands:** /help, /clear, /memory, /date, /creator, /export"
    elif cmd in ["/clear", "clear"]:
        st.session_state.messages = []
        return " Chat cleared!"
    elif cmd in ["/date", "date"]:
        return f" {datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}"
    elif "creator" in cmd or "/creator" in cmd:
        return " Created by Vishesh Sanghvi\nLinkedIn: https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/"
    elif cmd == "/memory":
        return f" Messages: {len(st.session_state.messages)} | Context: Last 30 messages"
    elif cmd == "/export":
        if not st.session_state.messages:
            return " No chat history"
        export = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        b64 = base64.b64encode(export.encode()).decode()
        return f"<a href='data:text/plain;base64,{b64}' download='chat.txt'> Download</a>"
    return None

# ---- SESSION STATE ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- SIDEBAR ----
with st.sidebar:
    st.title(" Settings")
    api_ok = bool(st.secrets.get("GEMINI_API_KEY", None) if hasattr(st, 'secrets') else os.environ.get("GEMINI_API_KEY"))
    st.success(" API Key OK") if api_ok else st.error(" API Key Missing")
    st.divider()
    st.metric("Messages", len(st.session_state.messages))
    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---- DISPLAY CHAT ----
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
if not st.session_state.messages:
    st.info(" Welcome! Type below or use /help for commands.")
for msg in st.session_state.messages:
    ts = msg['timestamp'].strftime('%H:%M:%S')
    if msg['role'] == 'user':
        st.markdown(f'<div class="user-message"><b> You:</b> {msg["content"]}</div><div class="timestamp">{ts}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><b> AI:</b> {msg["content"]}</div><div class="timestamp">{ts}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- INPUT ----
with st.form("input_form", clear_on_submit=True):
    user_input = st.text_area(" Your Message:", placeholder="Ask anything...", height=100)
    submitted = st.form_submit_button("Send ", use_container_width=True)
    
    if submitted and user_input.strip():
        cmd_resp = handle_commands(user_input.strip())
        if cmd_resp:
            st.session_state.messages.append({"role": "assistant", "content": cmd_resp, "timestamp": datetime.now()})
        else:
            st.session_state.messages.append({"role": "user", "content": user_input.strip(), "timestamp": datetime.now()})
            with st.spinner(" Thinking..."):
                ai_resp = get_response_from_api(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": ai_resp, "timestamp": datetime.now()})
        st.rerun()

st.markdown('<div class="footer"><hr>Created with  by Vishesh Sanghvi | <a href="https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/" target="_blank">LinkedIn</a></div>', unsafe_allow_html=True)
