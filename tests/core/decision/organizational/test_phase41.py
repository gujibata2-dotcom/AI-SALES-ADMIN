import unittest

from app.api.core.decision.organizational.contracts import (
    DecisionOption, DecisionRecord, EvidenceRef, EvidenceClass, Uncertainty, Reversibility,
)
from app.api.core.decision.organizational.evaluation import (
    authorization_level, authorize, HARD_CONSTRAINT, validate_constraints,
)
from app.api.core.decision.organizational.strategy import decision_quality, strategy_drift, StrategyRecord, StrategyRegistry


class Phase41SafetyTests(unittest.TestCase):
    def test_recommendation_is_not_authorization(self):
        evidence = [EvidenceRef("e1", EvidenceClass.EVIDENCE, "synthetic", False)]
        option = DecisionOption("A", "Option A", "meaningful difference")
        record = DecisionRecord("d1", "Synthetic decision", {}, ["g1"], [], evidence, [option], uncertainty=Uncertainty.UNCERTAIN)
        self.assertIsNone(record.selected_option)

    def test_high_risk_requires_human_approval(self):
        level = authorization_level(risk="HIGH", impact="HIGH", reversibility=Reversibility.REVERSIBLE, policy_allows=True)
        self.assertEqual(level.value, "HUMAN_APPROVAL_REQUIRED")
        self.assertFalse(authorize(level, None))
        self.assertTrue(authorize(level, {"authorized": True, "actor_reference": "human-ref"}))

    def test_prohibited_policy_blocks(self):
        level = authorization_level(risk="LOW", impact="LOW", reversibility=Reversibility.REVERSIBLE, policy_allows=False)
        self.assertEqual(level.value, "PROHIBITED")
        self.assertFalse(authorize(level, {"authorized": True}))

    def test_hard_constraint_blocks(self):
        constraints = [{"id": "c1", "mode": HARD_CONSTRAINT, "predicate": "policy_ok"}]
        self.assertEqual(validate_constraints(constraints, {"policy_ok": False}), ["c1"])

    def test_quality_does_not_equal_outcome(self):
        self.assertEqual(decision_quality(evidence_sufficient=True, assumptions_reasonable=True, risks_identified=True, authorization_correct=True, outcome_good=False), "GOOD_DECISION_BAD_OUTCOME")
        self.assertEqual(decision_quality(evidence_sufficient=False, assumptions_reasonable=True, risks_identified=True, authorization_correct=True, outcome_good=True), "INSUFFICIENT_EVIDENCE")

    def test_hindsight_preserves_history(self):
        registry = StrategyRegistry()
        strategy = StrategyRecord("s1", ["g1"], ["a1"], ["i1"], [], [], ["m1"], ["r1"])
        registry.register(strategy)
        adapted = registry.adapt("s1", trigger="new_evidence", reason="synthetic evidence changed an assumption", evidence_refs=["e1"])
        self.assertEqual(adapted.version, 2)
        self.assertEqual(len(registry.history("s1")), 2)

    def test_drift_without_basis_is_unknown(self):
        result = strategy_drift({"demand": 10}, {"demand": 20})
        self.assertEqual(result["strategy_drift_score"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
