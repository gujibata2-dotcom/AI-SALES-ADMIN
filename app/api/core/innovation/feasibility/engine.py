def assess_feasibility(technical, economic, operational, security, legal="UNKNOWN") -> dict:
    vals = [technical, economic, operational, security]
    if any(v == "NOT_FEASIBLE" for v in vals): result = "NOT_FEASIBLE"
    elif all(v == "FEASIBLE" for v in vals): result = "FEASIBLE"
    elif any(v == "UNKNOWN" for v in vals): result = "UNKNOWN"
    else: result = "PARTIALLY_FEASIBLE"
    return {"technical_feasibility":technical,"economic_feasibility":economic,"operational_feasibility":operational,"security_feasibility":security,"legal_feasibility_if_known":legal,"result":result}
