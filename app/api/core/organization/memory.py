"""Organizational memory is versioned and approval-gated."""

def learning_candidate(employee_id, evidence, proposed_rule):
    return {"employee_id":employee_id,"evidence":evidence,"proposed_rule":proposed_rule,"status":"CANDIDATE","requires_evaluation":True,"requires_approval":True}
