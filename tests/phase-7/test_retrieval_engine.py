from datetime import date

from app.knowledge.retrieval import KnowledgeChunk, RetrievalQuery, retrieve

TODAY = date(2026, 8, 12)


def test_active_source_is_retrieved():
    chunks = [KnowledgeChunk("src-1", "chunk-1", "price 699 baht per month", "active", language="en")]
    result = retrieve(RetrievalQuery("price 699", "en", "pricing", TODAY), chunks)
    assert result.state == "grounded"
    assert result.evidence[0].source_id == "src-1"


def test_expired_source_is_excluded():
    chunks = [KnowledgeChunk("src-old", "chunk-old", "price 699 baht", "active", effective_to=date(2026, 7, 31))]
    result = retrieve(RetrievalQuery("price 699", "en", "pricing", TODAY), chunks)
    assert result.state == "insufficient_evidence"


def test_archived_source_is_excluded():
    chunks = [KnowledgeChunk("src-archived", "chunk-1", "price 699", "archived")]
    result = retrieve(RetrievalQuery("price 699", "en", "pricing", TODAY), chunks)
    assert result.state == "insufficient_evidence"


def test_language_filter_prefers_requested_language():
    chunks = [
        KnowledgeChunk("src-th", "th-1", "ราคา 699 บาท", "active", language="th"),
        KnowledgeChunk("src-en", "en-1", "price 699 baht", "active", language="en"),
    ]
    result = retrieve(RetrievalQuery("price 699", "en", "pricing", TODAY), chunks)
    assert result.evidence[0].source_id == "src-en"


def test_missing_evidence_is_explicit():
    chunks = [KnowledgeChunk("src-1", "chunk-1", "refund policy", "active")]
    result = retrieve(RetrievalQuery("stock available", "en", "stock", TODAY), chunks)
    assert result.state == "insufficient_evidence"


def test_equal_relevance_disagreement_is_conflict():
    chunks = [
        KnowledgeChunk("src-a", "a-1", "price 699 baht", "active"),
        KnowledgeChunk("src-b", "b-1", "price 499 baht", "active"),
    ]
    result = retrieve(RetrievalQuery("price", "en", "pricing", TODAY), chunks)
    assert result.state == "conflict"
