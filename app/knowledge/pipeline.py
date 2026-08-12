"""End-to-end knowledge ingestion facade."""
from .index import KnowledgeIndex
from .ingestion import KnowledgeDocument, chunk, normalize


def ingest(document: KnowledgeDocument, index: KnowledgeIndex, max_chars: int = 500) -> int:
    normalized = normalize(document)
    chunks = chunk(normalized, max_chars=max_chars)
    index.upsert(chunks)
    return len(chunks)
