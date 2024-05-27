from openai import OpenAI
from sklearn import base
import streamlit as st
import requests

st.title("Quick API Chatbot")


base_url = "http://localhost:8000"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # curl コマンドでPOSTリクエストを送信
    response = requests.post(f"{base_url}/chat", json={"text": prompt})
    message = response.text

    with st.chat_message("assistant"):
        st.markdown(message)
    st.session_state.messages.append({"role": "assistant", "content": message})
