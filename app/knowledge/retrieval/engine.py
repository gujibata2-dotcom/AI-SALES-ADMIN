"""Deterministic, dependency-free Phase 7 retrieval engine."""
from datetime import date
import re
from .types import Evidence, KnowledgeChunk, RetrievalQuery, RetrievalResult


def _eligible(chunk: KnowledgeChunk, as_of: date) -> bool:
    if chunk.status != "active":
        return False
    if chunk.effective_from and as_of < chunk.effective_from:
        return False
    if chunk.effective_to and as_of > chunk.effective_to:
        return False
    return True


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"\w+", value.lower()) if token}


def _score(query: str, text: str) -> float:
    q = _tokens(query)
    t = _tokens(text)
    if not q or not t:
        return 0.0
    return len(q & t) / len(q)


def retrieve(query: RetrievalQuery, chunks: list[KnowledgeChunk], limit: int = 5) -> RetrievalResult:
    eligible = [c for c in chunks if _eligible(c, query.as_of)]
    if query.language:
        localized = [c for c in eligible if not c.language or c.language == query.language]
        if localized:
            eligible = localized

    ranked = sorted(
        ((c, _score(query.text, c.text)) for c in eligible),
        key=lambda item: item[1],
        reverse=True,
    )
    ranked = [(c, score) for c, score in ranked if score > 0][:limit]

    if not ranked:
        return RetrievalResult("insufficient_evidence", (), "No eligible evidence matched the query.")

    evidence = tuple(Evidence(c.source_id, c.chunk_id, score, c.text) for c, score in ranked)
    if len(evidence) > 1 and evidence[0].score == evidence[1].score and evidence[0].text != evidence[1].text:
        return RetrievalResult("conflict", evidence, "Multiple eligible sources have equal relevance and disagree.")
    return RetrievalResult("grounded", evidence)
