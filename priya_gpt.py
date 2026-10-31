
import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Priya GPT",
    page_icon="💬"
)

st.title("💜 Priya GPT")
st.caption("Your personal AI chatbot")

with st.expander("About Priya GPT", expanded=True):
    st.write(
        "Welcome to Priya GPT! I am an AI chatbot "
        "that can answer questions, explain Python, "
        "help with studies, and much more."
    )

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("Please configure your Gemini API key.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Priya GPT is thinking..."):
            try:
                history = []

                for message in st.session_state.messages:
                    role = (
                        "user"
                        if message["role"] == "user"
                        else "model"
                    )
                    history.append({
                        "role": role,
                        "parts": [{"text": message["content"]}]
                    })

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=history,
                    config={
                        "system_instruction":
                        "You are Priya GPT, a friendly and "
                        "helpful AI assistant. Give clear "
                        "and useful answers."
                    }
                )

                answer = response.text
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "AI response failed. Check your API key, "
                    "internet connection, and API quota."
                )
                st.caption(str(error))

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
