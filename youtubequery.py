from ingestion import IngestError, ingest_youtube_url
from vectorstore import (
    VectorStoreError,
    as_retriever,
    create_embeddings,
    index_chunks,
    search_chunks,
)


class YoutubeQuery:
    def __init__(self, gemini_api_key=None) -> None:
        self.embeddings = create_embeddings(gemini_api_key)
        self.vectorstore = None
        self.retriever = None

    def search(self, question: str):
        if self.retriever is None:
            return None
        return search_chunks(self.retriever, question)

    def ask(self, question: str) -> str:
        docs = self.search(question)
        if docs is None:
            return "Please, add a video."
        if not docs:
            return "No relevant transcript passages were found for that question."
        return "\n\n".join(doc.page_content for doc in docs)

    def ingest(self, url: str) -> str:
        try:
            chunks = ingest_youtube_url(url)
            self.vectorstore = index_chunks(chunks, self.embeddings)
            self.retriever = as_retriever(self.vectorstore)
        except IngestError as exc:
            return f"Error: {exc}"
        except VectorStoreError as exc:
            return f"Error: {exc}"
        return "Success"

    def forget(self) -> None:
        self.vectorstore = None
        self.retriever = None
