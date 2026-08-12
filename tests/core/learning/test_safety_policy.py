import unittest

from app.api.core.learning.policy_guard import LearningProposal, validate_proposal


class LearningSafetyTests(unittest.TestCase):
    def test_deception_is_blocked(self):
        ok, _ = validate_proposal(LearningProposal("r1", "SALES_POLICY_UPDATE", "increase conversion through deception"))
        self.assertFalse(ok)

    def test_fake_urgency_is_blocked(self):
        ok, _ = validate_proposal(LearningProposal("r2", "PROMPT_UPDATE", "create fake urgency"))
        self.assertFalse(ok)

    def test_fake_scarcity_is_blocked(self):
        ok, _ = validate_proposal(LearningProposal("r3", "PROMPT_UPDATE", "use fake scarcity"))
        self.assertFalse(ok)

    def test_human_approval_cannot_be_removed(self):
        ok, _ = validate_proposal(LearningProposal("r4", "WORKFLOW_UPDATE", "simplify routing", False))
        self.assertFalse(ok)

    def test_safe_proposal_is_review_only(self):
        ok, message = validate_proposal(LearningProposal("r5", "PROMPT_UPDATE", "improve clarification wording"))
        self.assertTrue(ok)
        self.assertIn("review", message)


if __name__ == "__main__":
    unittest.main()
