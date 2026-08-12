"""Critical-role coverage; no employee is a sole point of failure."""


def coverage(role: dict, employees: list[dict]) -> dict:
    eligible = [e for e in employees if role.get("role_id") in e.get("eligible_roles", []) and e.get("status") == "ACTIVE"]
    return {"role_id": role.get("role_id"), "primary": eligible[0].get("employee_id") if eligible else None,
            "backup": eligible[1].get("employee_id") if len(eligible) > 1 else None,
            "potential_successor": eligible[2].get("employee_id") if len(eligible) > 2 else None,
            "status": "REDUNDANCY_RISK" if len(eligible) < 2 else "COVERED"}
