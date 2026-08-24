import os

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

CHROMA_DIR = "chroma_db"
EMBEDDING_MODEL = "models/text-embedding-004"
RETRIEVE_K = 4


class VectorStoreError(RuntimeError):
    """Raised when embeddings or ChromaDB indexing fails."""


def create_embeddings(gemini_api_key: str) -> GoogleGenerativeAIEmbeddings:
    key = (gemini_api_key or "").strip()
    if not key:
        raise VectorStoreError("A Gemini API key is required for embeddings.")
    os.environ["GEMINI_API_KEY"] = key
    os.environ["GOOGLE_API_KEY"] = key
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=key,
    )


def _collection_name(video_id: str) -> str:
    safe = "".join(char for char in video_id if char.isalnum() or char in "-_")
    return f"yt_{safe or 'video'}"


def index_chunks(
    chunks: list[Document],
    embeddings: GoogleGenerativeAIEmbeddings,
    persist_directory: str = CHROMA_DIR,
) -> Chroma:
    if not chunks:
        raise VectorStoreError("No transcript chunks to index.")

    video_id = str(chunks[0].metadata.get("video_id", "video"))
    collection_name = _collection_name(video_id)

    try:
        client = chromadb.PersistentClient(path=persist_directory)
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass
        return Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            client=client,
            collection_name=collection_name,
        )
    except VectorStoreError:
        raise
    except Exception as exc:
        raise VectorStoreError("Failed to index transcript chunks in ChromaDB.") from exc


def as_retriever(vectorstore: Chroma, k: int = RETRIEVE_K):
    return vectorstore.as_retriever(search_kwargs={"k": k})


def search_chunks(retriever, query: str) -> list[Document]:
    if hasattr(retriever, "invoke"):
        return retriever.invoke(query)
    return retriever.get_relevant_documents(query)
