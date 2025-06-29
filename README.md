# 🧠 Groq-Powered Chatbot with Memory (Streamlit + ChromaDB)

This project is an interactive chatbot that uses:
- 🧠 **Groq API** for blazing-fast responses (Mixtral / LLaMA 3)
- 🗂️ **ChromaDB** for persistent memory (semantic search)
- 🌐 **Streamlit** for a simple chat interface
- 🤗 **SentenceTransformers** to embed user messages for recall

---

## 🚀 Features

- Remembers past user interactions
- Answers follow-up questions using vector memory
- Keeps memory persistent between sessions (via ChromaDB)
- Fully open-source, deployable to [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📦 Installation

1. **Clone this repo**
   ```bash
   git clone https://github.com/karthikwadeyar45/groq-chatbot.git
   cd groq-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   echo "GROQ_API_KEY=your_groq_key_here" > .env
   ```

---

## 🧠 Start ChromaDB Server

In a new terminal:

```bash
chroma run --path memory/chroma
```

This keeps your chatbot memory persistent.

---

## 🧪 Run Locally

```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this project to GitHub (don’t forget your `.gitignore`)
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"New app"** and choose your repo
4. In **Secrets** section, add:

```
GROQ_API_KEY=your-real-api-key-here
```

5. Click **Deploy**

---

## 📁 Project Structure

```
├── app.py                  # Main Streamlit app
├── .env                    # Your API key (ignored)            
├── memory/chroma/          # ChromaDB persistent memory
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🤝 Credits

Built with ❤️ using:
- [Groq](https://groq.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
