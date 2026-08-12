"""Priority components are explicit; no single opaque KPI decides priority."""
COMPONENTS = ("business_value", "urgency", "risk", "deadline", "dependency", "resource_cost", "strategic_alignment")

def priority_components(values: dict[str, float]) -> dict[str, float]:
    return {k: float(values[k]) for k in COMPONENTS if k in values}
