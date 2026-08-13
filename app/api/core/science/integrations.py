"""Phase 38 integration contracts; adapters are proposal-only and do not bypass governance."""

def knowledge_proposal(finding_id: str, classification: str, review: str, approval: str | None):
    publishable = classification == "SUPPORTED_BY_EVIDENCE" and review == "APPROVE" and bool(approval)
    return {"finding_id":finding_id,"publishable":publishable,"phase":3,"status":"PROPOSAL_ONLY" if not publishable else "APPROVED_PROPOSAL"}

def research_priority(importance, risk, information_gain, cost, feasibility, strategic_value):
    return {"importance":importance,"risk":risk,"expected_information_gain":information_gain,"cost":cost,"feasibility":feasibility,"strategic_value":strategic_value}

def innovation_handoff(finding_id: str, validated: bool):
    return {"finding_id":finding_id,"phase":37,"status":"OPPORTUNITY_CANDIDATE" if validated else "NOT_READY"}
