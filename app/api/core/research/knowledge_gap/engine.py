from typing import Dict, Any

def detect_gaps(known: list[str], unknown: list[str], importance: str = "MEDIUM") -> list[Dict[str, Any]]:
    return [{"gap_id": f"gap-{i+1}", "question": q, "importance": importance, "status": "KNOWLEDGE_GAP"} for i, q in enumerate(unknown)]

def failure_classification(reason: str) -> str:
    known = {"no_source": "NO_RELEVANT_SOURCE", "insufficient": "INSUFFICIENT_EVIDENCE", "conflict": "SOURCE_CONFLICT", "outdated": "OUTDATED_DATA", "tool": "TOOL_FAILURE", "retrieval": "RETRIEVAL_FAILURE", "scope": "SCOPE_FAILURE", "analysis": "ANALYSIS_FAILURE"}
    return known.get(reason, "UNKNOWN")
