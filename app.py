import streamlit as st
import os
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb import HttpClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Load GROQ API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB HttpClient (ensure `chroma run --path memory/chroma` is running)
chroma_client = HttpClient(host="localhost", port=8000)

# Embedding function for similarity search
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create persistent collection
collection = chroma_client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_function
)

# Streamlit UI
st.title("Groq Chatbot with Memory")
st.chat_message("assistant").write("Hi, how may I help you?")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

# --- Build context by filtering noisy memory ---
def build_context(user_query):
    try:
        results = collection.query(query_texts=[user_query], n_results=3)
        relevant_docs = [
            doc for doc in results["documents"][0]
            if doc and "your name is" not in doc.lower()
        ]
        past_memory = "\n\n".join(relevant_docs)

        return f"""You are a polite and helpful teaching assistant for a Data Science course.

Use the following past conversation memory to answer the current question:

{past_memory}

Now answer this: {user_query}
"""
    except Exception:
        return user_query

# --- Store new interaction in memory ---
def store_to_memory(user_input, bot_response):
    content = f"User: {user_input}\nAssistant: {bot_response}"
    new_id = f"id-{len(collection.get()['ids'])}"
    collection.add(documents=[content], ids=[new_id])

# --- Call Groq API ---
def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",  # You can also use "llama3-70b-8192"
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"Groq API Error: {response.status_code}")
        st.error(response.text)
        raise requests.exceptions.HTTPError(response.text)

    return response.json()["choices"][0]["message"]["content"]

# --- Handle user query ---
if user_input:
    st.chat_message("user").write(user_input)

    # Build prompt using filtered memory
    full_prompt = build_context(user_input)

    # Query Groq model
    bot_response = call_groq(full_prompt)
    st.chat_message("assistant").write(bot_response)

    # Store to session + memory
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    store_to_memory(user_input, bot_response)
