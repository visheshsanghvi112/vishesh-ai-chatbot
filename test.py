import streamlit as st
import requests
import json
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Vishesh GPT", page_icon="", layout="wide", initial_sidebar_state="expanded")

# Premium dark theme with green accents
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background-color: #000000;
        color: #00FF00;
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #00FF00;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
    }
    
    .main-header h1 {
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-size: 2.2em;
        margin: 0;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #00DD00;
        margin-top: 10px;
        font-family: 'Courier New', monospace;
    }
    
    /* Chat container */
    .chat-container {
        background: #0a0a0a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #00FF00;
        min-height: 450px;
        max-height: 600px;
        overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.1);
    }
    
    /* User message */
    .user-msg {
        background: linear-gradient(135deg, #1a3a1a 0%, #0d1f0d 100%);
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 4px solid #00FF00;
        margin: 12px 0;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
        animation: slideInRight 0.3s ease-out;
    }
    
    /* AI message */
    .ai-msg {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 4px solid #00DD00;
        margin: 12px 0;
        color: #FFFFFF;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 15px rgba(0, 221, 0, 0.2);
        animation: slideInLeft 0.3s ease-out;
    }
    
    .user-msg strong {
        color: #00FF00;
        font-size: 1.05em;
        display: block;
        margin-bottom: 8px;
    }
    
    .ai-msg strong {
        color: #00DD00;
        font-size: 1.05em;
        display: block;
        margin-bottom: 8px;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 0.75em;
        color: #006600;
        margin-top: 6px;
        opacity: 0.8;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 2px solid #00FF00;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    
    section[data-testid="stSidebar"] .stMetric {
        background: #1a1a1a;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #00FF00;
        margin: 8px 0;
    }
    
    section[data-testid="stSidebar"] .stMetric label {
        color: #00DD00 !important;
    }
    
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #00FF00 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #00FF00 0%, #00DD00 100%);
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
    }
    
    .stButton button:hover {
        background: #00FF00;
        box-shadow: 0 0 25px rgba(0, 255, 0, 0.5);
        transform: translateY(-2px);
    }
    
    /* Success/Error */
    .stSuccess, .stError {
        font-family: 'Courier New', monospace;
    }
    
    /* Divider */
    hr {
        border-color: #00FF00;
        opacity: 0.3;
    }
    
    /* Welcome screen */
    .welcome {
        text-align: center;
        padding: 60px 20px;
        color: #00FF00;
        font-family: 'Courier New', monospace;
    }
    
    .welcome h2 {
        color: #00FF00;
        text-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
        margin-bottom: 20px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #006600;
        font-family: 'Courier New', monospace;
        border-top: 1px solid #00FF00;
        margin-top: 30px;
    }
    
    .footer a {
        color: #00FF00;
        text-decoration: none;
        font-weight: bold;
    }
    
    .footer a:hover {
        color: #00DD00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00FF00;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00DD00;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1> VISHESH GPT - AI ASSISTANT</h1>
    <p> GEMINI 2.5 FLASH  NEURAL NETWORK ACTIVE  CONTEXT-AWARE</p>
</div>
""", unsafe_allow_html=True)

def get_ai_response(messages):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return " [SYSTEM ERROR] API Key not configured. Add GEMINI_API_KEY to Streamlit secrets."
    
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
            return f" [ERROR {resp.status_code}] {resp.text[:100]}"
    except Exception as e:
        return f" [SYSTEM ERROR] {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("###  CONTROL PANEL")
    
    try:
        has_key = bool(st.secrets.get("GEMINI_API_KEY"))
    except:
        has_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if has_key:
        st.success(" CONNECTION ESTABLISHED")
    else:
        st.error(" NO API CONNECTION")
    
    st.divider()
    
    st.metric(" MESSAGES", len(st.session_state.messages))
    st.metric(" MEMORY", f"{min(len(st.session_state.messages), 20)}/20")
    st.metric(" MODEL", "GEMINI 2.5")
    
    st.divider()
    
    if st.button(" CLEAR HISTORY", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    **CREATOR:**  
    Vishesh Sanghvi  
    [ LinkedIn Profile](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)
    """)

# Chat area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h2> SYSTEM READY</h2>
        <p>Neural network initialized and ready for interaction.</p>
        <p>Type your message below to begin conversation.</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    css_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    icon = " USER" if msg["role"] == "user" else " AI"
    timestamp = msg.get("timestamp", datetime.now()).strftime("%H:%M:%S")
    
    st.markdown(f"""
    <div class="{css_class}">
        <strong> {icon}</strong>
        <div>{msg["content"]}</div>
        <div class="timestamp">[{timestamp}]</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input(" Enter your message..."):
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    with st.spinner(" Processing neural network response..."):
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
    <p>Created by <a href="https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/" target="_blank">Vishesh Sanghvi</a> | Powered by Google Gemini 2.5 Flash</p>
    <p> NEURAL NETWORK ACTIVE   CONTEXT-AWARE   HIGH PERFORMANCE</p>
</div>
""", unsafe_allow_html=True)
