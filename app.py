import streamlit as st
import os
import requests
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB client setup
client = MongoClient(MONGODB_URI)
db = client["chatbot"]
collection = db["chat_memory"]

# Streamlit UI
st.title("💬 Groq Chatbot with MongoDB Memory")

# Ask for email
email = st.text_input("Enter your email to start chatting:")
if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    st.info("Please enter a valid email to begin.")
    st.stop()

# Use email as session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = email.strip().lower()

# Load message history from MongoDB
if "messages" not in st.session_state:
    stored = list(collection.find({"session_id": st.session_state.session_id}))
    st.session_state.messages = stored

# Display previous chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    collection.insert_one({"session_id": st.session_state.session_id, "role": "user", "content": user_input})

    # Prepare history (limit to last 20)
    history = [
        {"role": "system", "content": "You are a polite and helpful teaching assistant for a data science course."}
    ] + [
        {"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages[-20:]
    ]

    # Send request to Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": history
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        st.chat_message("assistant").write(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        collection.insert_one({"session_id": st.session_state.session_id, "role": "assistant", "content": assistant_reply})
    else:
        st.error(f"Error: Unable to get response from Groq API ({response.status_code})")
        st.code(response.text)