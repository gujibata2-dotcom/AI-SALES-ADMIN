"""In-memory knowledge index with deterministic upsert and search."""
from dataclasses import dataclass
from ..ingestion.types import DocumentChunk
from ..retrieval.types import KnowledgeChunk


@dataclass
class KnowledgeIndex:
    _chunks: dict[str, KnowledgeChunk]

    def __init__(self) -> None:
        self._chunks = {}

    def upsert(self, chunks: list[DocumentChunk]) -> None:
        for chunk in chunks:
            self._chunks[chunk.chunk_id] = KnowledgeChunk(
                source_id=chunk.source_id,
                chunk_id=chunk.chunk_id,
                text=chunk.text,
                status=chunk.status,
                effective_from=chunk.effective_from,
                effective_to=chunk.effective_to,
                language=chunk.language,
            )

    def get(self, chunk_id: str) -> KnowledgeChunk | None:
        return self._chunks.get(chunk_id)

    def all(self) -> list[KnowledgeChunk]:
        return list(self._chunks.values())

    def remove_source(self, source_id: str) -> int:
        ids = [key for key, value in self._chunks.items() if value.source_id == source_id]
        for key in ids:
            del self._chunks[key]
        return len(ids)

    def __len__(self) -> int:
        return len(self._chunks)
