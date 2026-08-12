"""Versioned domain -> capability -> skill -> subskill -> task graph."""


def skill_gap(required: dict, current: dict) -> list[dict]:
    gaps = []
    for skill, level in required.items():
        actual = current.get(skill, "NONE")
        if actual != level:
            gaps.append({"skill": skill, "required_level": level, "current_level": actual,
                         "gap_type": "KNOWLEDGE_GAP"})
    return gaps


def graph_node(domain: str, capability: str, skill: str, subskill: str | None = None) -> dict:
    return {"domain": domain, "capability": capability, "skill": skill, "subskill": subskill}
