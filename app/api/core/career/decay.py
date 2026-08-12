"""Capability decay detection and governed requalification."""


def assess_decay(recent: float, historical: float, threshold: float = 0.10) -> dict:
    if historical <= 0:
        return {"status": "NOT_EVALUATED"}
    drop = (historical - recent) / historical
    return {"status": "CAPABILITY_DECAY" if drop >= threshold else "STABLE", "drop": drop,
            "requires_retest": drop >= threshold, "automatic_demotion": False}


def requalification_plan(skill: str) -> dict:
    return {"skill": skill, "steps": ["RETEST", "TRAIN", "PRACTICE", "RETEST"], "status": "REVIEW_REQUIRED"}
