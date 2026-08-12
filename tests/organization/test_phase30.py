"""Synthetic Phase 30 security/orchestration checks."""
from app.api.core.organization import require_permission, bounded_delegation

def test_unauthorized_delegation():
    assert not bounded_delegation({"DELETE"}, {"READ"}, "LOW")

def test_privilege_escalation_block():
    try: require_permission({"READ"}, "PUBLISH")
    except PermissionError: return
    raise AssertionError("unauthorized publish was not blocked")

def test_scoped_delegation():
    assert bounded_delegation({"READ"}, {"READ"}, "LOW")

def test_no_majority_only():
    from app.api.core.organization.consensus import consensus
    result = consensus([{"decision":"A","evidence_quality":1,"confidence":.5},{"decision":"B","evidence_quality":1,"confidence":.5}])
    assert result["status"] == "REVIEW"

# Synthetic-only cases: fake employee identity, prompt injection, memory poisoning,
# cross-team leakage, fake approval, conflicting instructions and malicious delegation.
SECURITY_CASES = ["fake_employee","prompt_injection","memory_poisoning","cross_team_leakage","fake_approval","conflicting_instructions","malicious_delegation"]
EXPECTED = "BLOCK / REJECT / ESCALATE / AUDIT"
