"""Workforce planning from evidence, trends and critical-role coverage."""


def workforce_snapshot(employees: list[dict], roles: list[dict]) -> dict:
    active = [e for e in employees if e.get("status") == "ACTIVE"]
    covered = {r.get("role_id"): sum(r.get("role_id") in e.get("eligible_roles", []) for e in active) for r in roles}
    return {"active_employees": len(active), "role_coverage": covered,
            "critical_role_risks": [rid for rid, count in covered.items() if count < 2]}
