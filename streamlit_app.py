import requests
import streamlit as st
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="ChatABF", page_icon="🤖", layout="centered")
st.title("🤖 ChatABF")
st.caption("Powered by Groq + LLaMA 3.3, created by ABF")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"message": prompt}, timeout=30)
                response.raise_for_status()
                answer = response.json()["response"]
            except requests.exceptions.ConnectionError:
                answer = "⚠️ Could not connect to the backend. Is the server running?"
            except requests.exceptions.Timeout:
                answer = "⚠️ The request timed out. Please try again."
            except Exception:
                answer = "⚠️ An unexpected error occurred."
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
