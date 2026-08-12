def provenance(source_id: str, retrieved_at: str | None, query: str) -> dict:
    return {"source_id": source_id, "retrieved_at": retrieved_at, "query": query, "provenance_complete": bool(source_id and query)}
