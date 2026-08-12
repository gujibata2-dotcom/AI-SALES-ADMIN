"""Resource-aware workforce allocation."""

def within_budget(request, budget):
    return all(request.get(k, 0) <= budget.get(k, 0) for k in ("cost", "tokens", "time", "tool_calls", "employee_capacity"))


def priority(value, urgency, risk, customer_impact, deadline, dependency):
    return 2*value + urgency + 2*risk + customer_impact + deadline + dependency
