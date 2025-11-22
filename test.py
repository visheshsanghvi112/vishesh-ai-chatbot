import streamlit as st
import requests
import json
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Vishesh AI Chatbot", page_icon="", layout="wide")

st.markdown("""<style>
.user-msg {background:#2b5329;padding:10px;border-radius:8px;margin:5px 0;color:#fff}
.ai-msg {background:#1e3a5f;padding:10px;border-radius:8px;margin:5px 0;color:#fff}
</style>""", unsafe_allow_html=True)

st.title(" Vishesh AI Chatbot - Gemini 2.5 Flash")

def get_ai_response(messages):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return " API Key not configured. Add GEMINI_API_KEY to Streamlit secrets."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-latest:generateContent?key={api_key}"
    
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
    st.header(" Settings")
    try:
        has_key = bool(st.secrets.get("GEMINI_API_KEY"))
    except:
        has_key = bool(os.environ.get("GEMINI_API_KEY"))
    
    if has_key:
        st.success(" API Key OK")
    else:
        st.error(" No API Key")
    
    st.metric("Messages", len(st.session_state.messages))
    if st.button(" Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    css_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    icon = "" if msg["role"] == "user" else ""
    st.markdown(f'<div class="{css_class}">{icon} <b>{msg["role"].title()}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(" Thinking..."):
        response = get_ai_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown("---\n<center>Created by Vishesh Sanghvi | Powered by Gemini 2.5 Flash</center>", unsafe_allow_html=True)
