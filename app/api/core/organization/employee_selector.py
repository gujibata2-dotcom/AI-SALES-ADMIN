"""Least-privilege employee selection; provider-neutral."""

def select_employee(candidates, required_capabilities, required_permissions, risk):
    eligible = []
    for e in candidates:
        if e.get("status") != "ACTIVE": continue
        if not set(required_capabilities) <= set(e.get("capabilities", [])): continue
        if not set(required_permissions) <= set(e.get("permissions", [])): continue
        if risk == "CRITICAL" and not e.get("human_approved_critical", False): continue
        eligible.append(e)
    return sorted(eligible, key=lambda e: (-e.get("performance", 0), e.get("cost", 10), e.get("latency", 10)))
