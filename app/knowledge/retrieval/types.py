"""Phase 7 retrieval contracts."""
from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional

SourceStatus = Literal["active", "expired", "archived"]
RetrievalState = Literal["grounded", "partial", "insufficient_evidence", "conflict"]

@dataclass(frozen=True)
class KnowledgeChunk:
    source_id: str
    chunk_id: str
    text: str
    status: SourceStatus
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    language: Optional[str] = None

@dataclass(frozen=True)
class RetrievalQuery:
    text: str
    language: str
    intent: str
    as_of: date

@dataclass(frozen=True)
class Evidence:
    source_id: str
    chunk_id: str
    score: float
    text: str

@dataclass(frozen=True)
class RetrievalResult:
    state: RetrievalState
    evidence: tuple[Evidence, ...]
    reason: Optional[str] = None
