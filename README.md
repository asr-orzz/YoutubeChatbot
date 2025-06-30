
````markdown
# 🎬 YoutubeChatbot

A powerful chatbot that lets you interact with any **YouTube video** using **LangChain**, **OpenAI**, and **Streamlit**. Just paste a YouTube video URL and start chatting — ask questions, extract insights, or summarize content.

![Made with LangChain and OpenAI](https://img.shields.io/badge/Made%20with-LangChain%20%26%20OpenAI-blue)
![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

---

## ✨ Features

- 🔗 Paste a YouTube URL and ingest video content
- 💬 Chat with the video transcript via a simple UI
- 🧠 Vector store with ChromaDB for fast retrieval
- 🤖 OpenAI-powered Q&A and summarization
- 📱 Minimal setup, runs in CLI or web UI

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/asr-orzz/YoutubeChatbot.git
cd YoutubeChatbot
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set OpenAI API Key

Set your OpenAI API key in your terminal:

```bash
export OPENAI_API_KEY="your-openai-api-key"  # macOS/Linux
set OPENAI_API_KEY="your-openai-api-key"     # Windows
```

Or enter it in the input field in the web UI.

---

## 🧪 How to Use

### CLI Mode

Edit `chat_youtube.py` and update the video URL and query:

```bash
python chat_youtube.py
```

### Streamlit Web App

```bash
streamlit run streamlitui.py
```

Then open the provided local URL in your browser.
You can input your API key and video URL directly in the app.

---

## 📂 Project Structure

| File               | Description                                  |
| ------------------ | -------------------------------------------- |
| `chat_youtube.py`  | Command-line chatbot example.                |
| `streamlitui.py`   | Streamlit-based chatbot UI.                  |
| `youtubequery.py`  | Core class handling ingestion and retrieval. |
| `requirements.txt` | Python dependencies.                         |

---

## 📍 Sample Queries

* “What is this video about?”
* “Summarize the main points.”
* “What did the speaker say about climate change?”

---

## 🔧 To-Do (Coming Soon)

* [ ] Multiple video ingestion
* [ ] Save chat history
* [ ] Support for other languages
* [ ] Streamlit file upload for local transcripts

---



