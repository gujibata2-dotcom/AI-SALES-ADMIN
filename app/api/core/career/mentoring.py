"""Mentoring uses verified capability and permission evidence only."""


def mentor_match(mentor: dict, learner: dict, skill: str) -> dict:
    verified = skill in mentor.get("verified_skills", [])
    permitted = skill in mentor.get("mentor_permissions", [])
    need = skill in learner.get("skill_gaps", [])
    return {"mentor_id": mentor.get("employee_id"), "learner_id": learner.get("employee_id"),
            "skill": skill, "eligible": verified and permitted and need}
