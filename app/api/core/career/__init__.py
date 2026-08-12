"""Phase 32 career, specialization and continuous mastery engine."""

LEVELS = ("TRAINEE", "JUNIOR", "PROFESSIONAL", "SENIOR", "EXPERT", "AUTONOMOUS", "SUPERHUMAN_SPECIALIST", "PERMANENT")
SKILL_LEVELS = ("NONE", "BASIC", "WORKING", "ADVANCED", "EXPERT", "MASTERED")
MASTERY_LEVELS = ("NOVICE", "DEVELOPING", "COMPETENT", "ADVANCED", "EXPERT", "SPECIALIST", "MASTERED")


def evidence_status(evidence: dict) -> str:
    if not evidence or evidence.get("status") in (None, "NOT_EVALUATED"):
        return "NOT_EVALUATED"
    return evidence.get("status", "INCONCLUSIVE")


def promotion_eligible(profile: dict, required: dict) -> bool:
    if profile.get("status") != "ACTIVE":
        return False
    return all(profile.get("competencies", {}).get(k, 0) >= v for k, v in required.get("competencies", {}).items())


def specialization_ready(evidence: list[dict], minimum_samples: int) -> bool:
    verified = [e for e in evidence if e.get("verified") is True]
    return len(verified) >= minimum_samples and all(e.get("reliability", 0) >= 0.9 for e in verified)


def decay_detected(recent: float, historical: float, threshold: float = 0.10) -> bool:
    return historical > 0 and (historical - recent) / historical >= threshold
