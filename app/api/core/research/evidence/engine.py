from ..models import Evidence

def extract(claim: str, source_id: str, context: str) -> Evidence:
    return Evidence("", claim, source_id, "INSUFFICIENT", "WEAK", context, confidence=None)
