"""Synthetic, privacy-safe Phase 32 tests."""
from app.api.core.career import decay_detected, specialization_ready
from app.api.core.career.skill_graph import skill_gap
from app.api.core.career.role_matching import match_role


def test_role_matching_exposes_components():
    result = match_role({"capabilities": ["CODING"]}, {"role_id": "software", "required_capabilities": ["CODING"]})
    assert result["capability_fit"] == 1.0
    assert "reliability_fit" in result


def test_skill_gap_is_explicit():
    gaps = skill_gap({"testing": "ADVANCED"}, {"testing": "BASIC"})
    assert gaps[0]["gap_type"] == "KNOWLEDGE_GAP"


def test_specialization_needs_repeated_verified_evidence():
    evidence = [{"verified": True, "reliability": .95} for _ in range(5)]
    assert specialization_ready(evidence, 5)
    assert not specialization_ready(evidence[:1], 5)


def test_decay_is_detected_without_auto_demotion():
    assert decay_detected(.7, .9)


def test_missing_evidence_is_not_evaluated():
    from app.api.core.career import evidence_status
    assert evidence_status({}) == "NOT_EVALUATED"
