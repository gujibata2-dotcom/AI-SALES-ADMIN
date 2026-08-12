"""Phase 7 knowledge ingestion contracts."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class KnowledgeDocument:
    source_id: str
    title: str
    text: str
    language: str
    status: str = "active"
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    source_uri: Optional[str] = None

@dataclass(frozen=True)
class NormalizedDocument:
    source_id: str
    title: str
    text: str
    language: str
    status: str
    effective_from: Optional[date]
    effective_to: Optional[date]
    source_uri: Optional[str]

@dataclass(frozen=True)
class DocumentChunk:
    source_id: str
    chunk_id: str
    text: str
    language: str
    status: str
    effective_from: Optional[date]
    effective_to: Optional[date]
    source_uri: Optional[str]
