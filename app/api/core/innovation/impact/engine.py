def assess_impact(**dimensions) -> dict:
    allowed = ("customer_impact","business_impact","employee_impact","organization_impact","social_impact","environmental_impact_if_relevant")
    return {"dimensions": {k: dimensions.get(k, "UNKNOWN") for k in allowed}, "numeric_impact": None}
