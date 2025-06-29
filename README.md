
# 🧠 Streamlit Chatbot with MongoDB Memory and Groq API

This is a Streamlit-based chatbot that:
- Uses Groq's `llama3-70b-8192` model for responses
- Stores conversation history in MongoDB Atlas
- Recalls memory across sessions

---

## 🚀 Features

- Interactive chat UI
- Persistent memory using MongoDB
- Full history recall (scoped per session)
- Free-tier friendly (Streamlit + MongoDB Atlas)

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/karthikwadeyar45/groq-chatbot.git
cd groq-chatbot
```

---

### 2. Create a `.env` File

Create a `.env` file in the root directory and add:

```env
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_uri
```

> You can get your MongoDB URI from [https://cloud.mongodb.com](https://cloud.mongodb.com)

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the App Locally

```bash
streamlit run app.py
```

---

### 5. Deploy to Streamlit Cloud

- Push your code to GitHub
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Create a new app and connect your GitHub repo
- Add your secrets under **App Settings > Secrets**:

```
GROQ_API_KEY = your_groq_key
MONGODB_URI = your_mongo_uri
```

---

## 📁 Folder Structure

```
├── app.py
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔐 Environment Variables

- `GROQ_API_KEY`: Your Groq API Key
- `MONGODB_URI`: Your MongoDB Atlas connection URI

---