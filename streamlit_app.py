import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Agent AI",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agent AI")
st.caption("Powered by Groq + LLaMA 3.3")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):

    # Add user message to history and render it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the backend
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

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})