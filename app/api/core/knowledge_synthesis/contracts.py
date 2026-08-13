"""Phase 39 knowledge synthesis contracts.
Pure standard-library helpers; no network/provider dependency.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

class ClaimType(str, Enum):
    FACT='FACT'; OBSERVATION='OBSERVATION'; INFERENCE='INFERENCE'; HYPOTHESIS='HYPOTHESIS'; OPINION='OPINION'; PREDICTION='PREDICTION'; UNKNOWN='UNKNOWN'

class KnowledgeStatus(str, Enum):
    RAW='RAW'; UNVERIFIED='UNVERIFIED'; PARTIALLY_VERIFIED='PARTIALLY_VERIFIED'; VERIFIED='VERIFIED'; CONTESTED='CONTESTED'; OUTDATED='OUTDATED'; SUPERSEDED='SUPERSEDED'; REJECTED='REJECTED'; UNKNOWN='UNKNOWN'; STALE='STALE'; REVERIFY_REQUIRED='REVERIFY_REQUIRED'

@dataclass(frozen=True)
class Evidence:
    evidence_id: str; claim: str; source: str; source_type: str; timestamp: str; method: str
    relevance: float; quality: float; independence: float; confidence: float; limitations: tuple[str,...]=()

@dataclass
class KnowledgeRecord:
    knowledge_id: str; title: str; statement: str; domain: str; source: list[str]
    evidence: list[str]; confidence: float; scope: str; limitations: list[str]
    version: int = 1; status: KnowledgeStatus = KnowledgeStatus.RAW
    provenance: list[str] = field(default_factory=list)

class KnowledgeRegistry:
    """In-memory contract used by tests/adapters. Production persistence belongs to the existing data layer."""
    def __init__(self) -> None:
        self._records: dict[str, KnowledgeRecord] = {}
        self._history: dict[str, list[KnowledgeRecord]] = {}

    def register(self, record: KnowledgeRecord) -> None:
        if not record.provenance and record.status == KnowledgeStatus.VERIFIED:
            raise ValueError('verified knowledge requires provenance')
        self._records[record.knowledge_id] = record
        self._history.setdefault(record.knowledge_id, []).append(record)

    def get(self, knowledge_id: str) -> KnowledgeRecord | None:
        return self._records.get(knowledge_id)

    def history(self, knowledge_id: str) -> tuple[KnowledgeRecord, ...]:
        return tuple(self._history.get(knowledge_id, ()))

    def rollback(self, knowledge_id: str, version: int) -> KnowledgeRecord:
        candidates = [r for r in self._history.get(knowledge_id, ()) if r.version == version]
        if not candidates:
            raise KeyError(f'unknown version: {knowledge_id}:{version}')
        restored = candidates[0]
        self._records[knowledge_id] = restored
        self._history[knowledge_id].append(restored)
        return restored

def classify_claim(has_evidence: bool, observed_directly: bool=False, inferential: bool=False) -> ClaimType:
    if not has_evidence: return ClaimType.UNKNOWN
    if observed_directly: return ClaimType.OBSERVATION
    if inferential: return ClaimType.INFERENCE
    return ClaimType.FACT

def should_verify(evidence: Iterable[Evidence]) -> bool:
    items = list(evidence)
    return bool(items) and all(0 <= e.confidence <= 1 and e.source and e.claim for e in items)

def preserve_external_content_as_data(content: Any) -> dict[str, Any]:
    return {'data': content, 'instructions_trusted': False}
