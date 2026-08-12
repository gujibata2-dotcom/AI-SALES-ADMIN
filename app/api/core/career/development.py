"""Development planning from measured skill gaps; production execution is out of scope."""

ALLOWED_PRACTICE = ("SANDBOX", "SYNTHETIC", "HISTORICAL_ANONYMIZED", "EDGE_CASE", "STRESS")


def build_plan(employee_id: str, target_role: str, gaps: list[dict], deadline: str | None = None) -> dict:
    return {"development_plan_id": f"dp:{employee_id}:{target_role}", "employee_id": employee_id,
            "target_role": target_role, "skill_gaps": gaps, "training_tasks": gaps,
            "practice_tasks": [{**g, "environment": "SANDBOX"} for g in gaps],
            "benchmarks": [], "success_criteria": [], "deadline": deadline, "status": "DRAFT"}


def training_effective(before: float, after: float, minimum_gain: float = 0.0) -> bool:
    return after - before > minimum_gain
