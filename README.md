# YouTubeChatbot

A conversational AI for chatting with YouTube video content. It fetches the video transcript, chunks it with overlap, embeds the chunks, stores them in ChromaDB, and answers questions with Gemini through a Streamlit chat UI.

## Tech stack

- **Python** and **LangChain** for the ingestion and retrieval pipeline
- **Gemini** for embeddings and question answering
- **ChromaDB** for vector storage and semantic search
- **Streamlit** for the live chat interface

## Features

- Fetch and parse YouTube transcripts from a video URL
- Split transcripts with overlap and context windows
- Index chunks in ChromaDB for fast semantic search
- Ask questions about the video in a Streamlit chat UI
- Keep the Gemini API key out of source control

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/asr-orzz/YoutubeChatbot.git
cd YoutubeChatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Gemini API key

Copy the example env file and add a key from [Google AI Studio](https://aistudio.google.com/apikey):

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=your-gemini-api-key
```

You can also enter the key in the Streamlit sidebar. Do not commit `.env`.

## How to use

```bash
streamlit run streamlitui.py
```

Open the local URL, paste a YouTube video link, wait for ingestion, then ask questions such as:

- What is this video about?
- Summarize the main points.
- What did the speaker say about climate change?

## Project structure

| File | Description |
| --- | --- |
| `ingestion.py` | YouTube URL parsing, transcript fetch, and overlap chunking |
| `vectorstore.py` | Gemini embeddings, ChromaDB indexing, and semantic search |
| `youtubequery.py` | Transcript ingestion, embeddings, ChromaDB, and Gemini Q&A |
| `streamlitui.py` | Streamlit chat UI and API key handling |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for the Gemini API key |

## Notes

- A video must have captions or an auto-generated transcript.
- Only Gemini is used for LLM and embedding calls.
