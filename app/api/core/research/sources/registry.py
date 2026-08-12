from ..models import Source

def register(source: Source) -> dict:
    return {"source_id": source.source_id, "source_type": source.source_type, "trust_status": source.trust_status, "verification_status": source.verification_status, "quality_dimensions": {"authority": source.authority, "relevance": source.relevance, "recency": source.recency, "methodology": source.methodology, "transparency": source.transparency, "independence": source.independence}}
