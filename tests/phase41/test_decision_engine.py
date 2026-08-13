import unittest
from app.api.core.decision_engine.contracts import decision_quality_class
from app.api.core.decision_engine.safety import authorization_level, decision_from_recommendation, execution_handoff

class Phase41SafetyTests(unittest.TestCase):
    def test_recommendation_cannot_bypass_authorization(self):
        with self.assertRaises(PermissionError): decision_from_recommendation({"decision_id":"d1"})
    def test_policy_conflict_is_prohibited(self):
        self.assertEqual(authorization_level(risk="LOW", impact="LOW", irreversible=False, policy_allows=False), "PROHIBITED")
    def test_high_impact_requires_review(self):
        self.assertEqual(authorization_level(risk="HIGH", impact="HIGH", irreversible=False, policy_allows=True), "HUMAN_APPROVAL_REQUIRED")
    def test_execution_boundary(self):
        with self.assertRaises(PermissionError): execution_handoff({"decision_id":"d1", "state":"RECOMMENDATION"})
    def test_quality_is_not_outcome_only(self):
        self.assertEqual(decision_quality_class(evidence_sufficient=True, decision_sound=True, outcome_good=False), "GOOD_DECISION_BAD_OUTCOME")
        self.assertEqual(decision_quality_class(evidence_sufficient=False, decision_sound=True, outcome_good=True), "INSUFFICIENT_EVIDENCE")

if __name__ == "__main__": unittest.main()
