from app.knowledge.ingestion import KnowledgeDocument, chunk, normalize


def test_normalize_whitespace_and_line_endings():
    doc = KnowledgeDocument("src-1", "  Pricing  ", "price   699\r\n\r\n\r\nmonthly", "EN")
    result = normalize(doc)
    assert result.title == "Pricing"
    assert result.language == "en"
    assert result.text == "price 699\n\nmonthly"


def test_normalize_rejects_empty_text():
    try:
        normalize(KnowledgeDocument("src-1", "Empty", "   ", "en"))
        assert False
    except ValueError as exc:
        assert "empty" in str(exc).lower()


def test_chunk_preserves_provenance_and_order():
    doc = normalize(KnowledgeDocument("src-9", "FAQ", "first paragraph\n\nsecond paragraph", "en"))
    chunks = chunk(doc, max_chars=50)
    assert [c.chunk_id for c in chunks] == ["src-9:1", "src-9:2"]
    assert all(c.source_id == "src-9" for c in chunks)


def test_long_paragraph_is_split():
    doc = normalize(KnowledgeDocument("src-2", "Long", "x" * 120, "en"))
    chunks = chunk(doc, max_chars=50)
    assert len(chunks) == 3
    assert all(len(c.text) <= 50 for c in chunks)
