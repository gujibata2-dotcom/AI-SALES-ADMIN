from datetime import date

from app.knowledge import KnowledgeIndex, ingest
from app.knowledge.ingestion import KnowledgeDocument
from app.knowledge.retrieval import RetrievalQuery, retrieve


def test_ingest_indexes_chunks_and_retrieve_uses_index():
    index = KnowledgeIndex()
    count = ingest(KnowledgeDocument("src-10", "Pricing", "Monthly price is 699 baht.", "en"), index)
    assert count == 1
    result = retrieve(
        RetrievalQuery("monthly price 699", "en", "pricing", date(2026, 8, 12)),
        index.all(),
    )
    assert result.state == "grounded"
    assert result.evidence[0].source_id == "src-10"
    assert result.evidence[0].chunk_id == "src-10:1"


def test_upsert_is_idempotent_for_same_chunk_ids():
    index = KnowledgeIndex()
    doc = KnowledgeDocument("src-11", "FAQ", "Refunds are available within seven days.", "en")
    ingest(doc, index)
    ingest(doc, index)
    assert len(index) == 1


def test_remove_source_removes_all_chunks():
    index = KnowledgeIndex()
    doc = KnowledgeDocument("src-12", "Long", "a" * 120, "en")
    ingest(doc, index, max_chars=50)
    assert len(index) == 3
    removed = index.remove_source("src-12")
    assert removed == 3
    assert len(index) == 0
