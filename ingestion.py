import re
from urllib.parse import parse_qs, urlparse

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


class IngestError(ValueError):
    """Raised when a YouTube URL cannot be parsed or a transcript cannot be fetched."""


def extract_video_id(url: str) -> str:
    raw = (url or "").strip()
    if not raw:
        raise IngestError("Enter a YouTube video URL.")
    if YOUTUBE_ID_RE.match(raw):
        return raw

    parsed = urlparse(raw)
    host = (parsed.netloc or "").lower()
    path_parts = [part for part in parsed.path.split("/") if part]
    video_id = ""

    if "youtu.be" in host:
        video_id = path_parts[0] if path_parts else ""
    elif "youtube" in host:
        query_id = parse_qs(parsed.query).get("v", [""])[0]
        if query_id:
            video_id = query_id
        elif len(path_parts) >= 2 and path_parts[0] in {"embed", "shorts", "live", "v"}:
            video_id = path_parts[1]

    video_id = video_id.split("?")[0].split("&")[0]
    if not YOUTUBE_ID_RE.match(video_id):
        raise IngestError("Could not parse a YouTube video ID from that URL.")
    return video_id


def _snippet_start_at_offset(snippets, offset: int) -> float:
    cursor = 0
    last_start = 0.0
    for snippet in snippets:
        text = snippet.text.strip()
        if not text:
            continue
        last_start = float(snippet.start)
        next_cursor = cursor + len(text) + 1
        if offset < next_cursor:
            return last_start
        cursor = next_cursor
    return last_start


def _fetch_transcript(video_id: str):
    api = YouTubeTranscriptApi()
    try:
        return api.fetch(video_id, languages=["en", "en-US", "en-GB"])
    except YouTubeTranscriptApiException:
        pass

    try:
        transcript_list = api.list(video_id)
        try:
            return transcript_list.find_transcript(["en", "en-US", "en-GB"]).fetch()
        except YouTubeTranscriptApiException:
            transcript = next(iter(transcript_list), None)
            if transcript is None:
                raise IngestError("No transcript is available for this video.")
            if getattr(transcript, "is_translatable", False):
                try:
                    return transcript.translate("en").fetch()
                except YouTubeTranscriptApiException:
                    pass
            return transcript.fetch()
    except IngestError:
        raise
    except YouTubeTranscriptApiException as exc:
        raise IngestError(
            "Could not fetch a transcript. The video may have captions disabled."
        ) from exc


def fetch_transcript_document(url: str) -> Document:
    video_id = extract_video_id(url)
    fetched = _fetch_transcript(video_id)
    snippets = [snippet for snippet in fetched if snippet.text.strip()]
    if not snippets:
        raise IngestError("The transcript for this video is empty.")

    page_content = " ".join(snippet.text.strip() for snippet in snippets)
    start = float(snippets[0].start)
    end = float(snippets[-1].start + snippets[-1].duration)
    return Document(
        page_content=page_content,
        metadata={
            "source": f"https://www.youtube.com/watch?v={video_id}",
            "video_id": video_id,
            "language": getattr(fetched, "language_code", "en"),
            "start": start,
            "end": end,
            "snippets": snippets,
        },
    )


def chunk_transcript(
    document: Document,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    snippets = document.metadata.pop("snippets", [])
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents([document])
    for chunk in chunks:
        start_index = chunk.metadata.get("start_index", 0)
        chunk.metadata["start"] = _snippet_start_at_offset(snippets, start_index)
        chunk.metadata["video_id"] = document.metadata.get("video_id", "")
        chunk.metadata["source"] = document.metadata.get("source", "")
        chunk.metadata["language"] = document.metadata.get("language", "en")
    return chunks


def ingest_youtube_url(
    url: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    document = fetch_transcript_document(url)
    chunks = chunk_transcript(document, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        raise IngestError("Could not split the transcript into searchable chunks.")
    return chunks
