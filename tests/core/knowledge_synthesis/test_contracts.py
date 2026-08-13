from app.api.core.knowledge_synthesis import validate_knowledge, classify_claim, should_require_human_review


def test_verified_knowledge_requires_evidence():
    record = {"knowledge_id":"k1","title":"x","statement":"x","domain":"test","evidence":[],"confidence":0.9,"scope":"test","limitations":[],"version":1,"status":"VERIFIED"}
    assert "verified_without_evidence" in validate_knowledge(record)


def test_unknown_when_uncertain_without_evidence():
    assert classify_claim(False, is_explicitly_uncertain=True) == "UNKNOWN"


def test_high_risk_requires_human_review():
    assert should_require_human_review(impact=0.2, risk=0.9)
