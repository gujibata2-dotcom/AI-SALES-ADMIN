"""Phase 31 capability benchmark, evaluation and promotion engine."""

LEVELS = ("TRAINEE", "JUNIOR", "PROFESSIONAL", "SENIOR", "EXPERT", "AUTONOMOUS", "SUPERHUMAN_SPECIALIST", "PERMANENT")
CAPABILITIES = ("REASONING", "CODING", "RESEARCH", "WRITING", "ANALYSIS", "PLANNING", "PROBLEM_SOLVING", "CUSTOMER_SUPPORT", "SALES", "LANGUAGE", "MULTIMODAL", "DATA_ANALYSIS", "TOOL_USE", "AGENTIC_EXECUTION", "VERIFICATION", "CREATIVITY", "MEMORY", "LEARNING", "COLLABORATION", "SECURITY")
RESULTS = ("NOT_EVALUATED", "PASS", "FAIL", "INCONCLUSIVE")


def require_evidence(evidence: dict) -> None:
    if not evidence or evidence.get("result") == "NOT_EVALUATED":
        raise ValueError("NOT_EVALUATED: evidence required")


def superhuman_candidate(ai: dict, human: dict) -> bool:
    if ai.get("sample_size", 0) < human.get("minimum_sample_size", 1):
        return False
    if ai.get("confidence", 0) < human.get("confidence_level", 0):
        return False
    return all(ai.get(k, 0) > human.get(k, 0) for k in ("accuracy", "quality", "reliability"))


def promotion_recommendation(level: str, evidence: dict) -> str:
    if evidence.get("result") in ("NOT_EVALUATED", "INCONCLUSIVE"):
        return "HOLD"
    return "RECOMMEND" if evidence.get("meets_level", False) else "HOLD"
