"""Evidence-gated promotion; high-risk and superhuman claims require review."""
LEVELS = ("TRAINEE", "JUNIOR", "PROFESSIONAL", "SENIOR", "EXPERT", "AUTONOMOUS", "SUPERHUMAN_SPECIALIST", "PERMANENT")

REQUIRED = ("evaluation_ids", "sample_size", "reliability", "safety", "result", "limitations")


def recommend(current_level: str, evidence: dict, target_level: str) -> dict:
    missing = [k for k in REQUIRED if k not in evidence]
    if missing or evidence.get("result") in ("NOT_EVALUATED", "INCONCLUSIVE"):
        return {"status": "HOLD", "reason": "insufficient evidence", "missing": missing}
    if target_level == "SUPERHUMAN_SPECIALIST":
        return {"status": "HUMAN_REVIEW_REQUIRED", "reason": "superhuman claim requires defined human baseline"}
    if evidence.get("meets_level") and evidence.get("safety", 0) >= 0.95 and evidence.get("reliability", 0) >= 0.95:
        return {"status": "RECOMMEND", "from": current_level, "to": target_level}
    return {"status": "HOLD", "reason": "threshold not met"}
