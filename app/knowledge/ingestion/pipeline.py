"""Deterministic normalization and chunking for trusted knowledge."""
import re
from .types import DocumentChunk, KnowledgeDocument, NormalizedDocument


def normalize(document: KnowledgeDocument) -> NormalizedDocument:
    text = document.text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        raise ValueError("Knowledge document text cannot be empty")
    if not document.source_id.strip():
        raise ValueError("source_id cannot be empty")
    return NormalizedDocument(
        source_id=document.source_id.strip(),
        title=document.title.strip(),
        text=text,
        language=document.language.strip().lower(),
        status=document.status,
        effective_from=document.effective_from,
        effective_to=document.effective_to,
        source_uri=document.source_uri,
    )


def chunk(document: NormalizedDocument, max_chars: int = 500) -> list[DocumentChunk]:
    if max_chars < 50:
        raise ValueError("max_chars must be at least 50")
    paragraphs = [p.strip() for p in document.text.split("\n\n") if p.strip()]
    chunks: list[DocumentChunk] = []
    buffer = ""
    index = 1
    for paragraph in paragraphs:
        if buffer and len(buffer) + 2 + len(paragraph) > max_chars:
            chunks.append(_make_chunk(document, buffer, index))
            index += 1
            buffer = ""
        if len(paragraph) <= max_chars:
            buffer = paragraph if not buffer else f"{buffer}\n\n{paragraph}"
        else:
            for start in range(0, len(paragraph), max_chars):
                piece = paragraph[start:start + max_chars].strip()
                if piece:
                    chunks.append(_make_chunk(document, piece, index))
                    index += 1
            buffer = ""
    if buffer:
        chunks.append(_make_chunk(document, buffer, index))
    return chunks


def _make_chunk(document: NormalizedDocument, text: str, index: int) -> DocumentChunk:
    return DocumentChunk(
        source_id=document.source_id,
        chunk_id=f"{document.source_id}:{index}",
        text=text,
        language=document.language,
        status=document.status,
        effective_from=document.effective_from,
        effective_to=document.effective_to,
        source_uri=document.source_uri,
    )
