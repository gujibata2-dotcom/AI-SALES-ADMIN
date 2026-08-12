import unittest
from app.api.core.operations.models import *
from app.api.core.operations.gateway import ActionGateway
from app.api.core.operations.planner import PlanValidator, PlanRejected
from app.api.core.operations.executor import ExecutionEngine


def action(autonomy=AutonomyLevel.L3, approved=True, cost=0, key="k"):
    return ActionRequest("a", "draft", "internal", {}, "agent", RiskLevel.LOW_RISK,
        Authorization("p","policy",autonomy,approved,False), ("internal",),("draft",),(),key,cost,30,2)

class Phase24SafetyTests(unittest.TestCase):
    def test_permission_denied(self): self.assertFalse(ActionGateway(10).authorize(action(approved=False)).allowed)
    def test_l5_blocked(self): self.assertFalse(ActionGateway(10).authorize(action(AutonomyLevel.L5)).allowed)
    def test_budget_blocked(self): self.assertFalse(ActionGateway(1).authorize(action(cost=2)).allowed)
    def test_duplicate_blocked(self):
        g=ActionGateway(10); a=action(); self.assertTrue(g.authorize(a).allowed); g.record(a); self.assertFalse(g.authorize(a).allowed)
    def test_kill_switch(self):
        g=ActionGateway(10); g.stop(); self.assertFalse(g.authorize(action()).allowed)
    def test_circular_plan_blocked(self):
        a=action(); p=ExecutionPlan("p","x",(PlanTask("a",("b",),(a,)),PlanTask("b",("a",),(a,))))
        with self.assertRaises(PlanRejected): PlanValidator.validate(p)
    def test_missing_dependency_blocked(self):
        p=ExecutionPlan("p","x",(PlanTask("a",("missing",),(action(),)),))
        with self.assertRaises(PlanRejected): PlanValidator.validate(p)
    def test_end_to_end_success(self):
        a=action(); p=ExecutionPlan("p","x",(PlanTask("a",(),(a,)),)); r=ExecutionEngine(ActionGateway(10)).run("e",p)
        self.assertEqual(r.verification, VerificationStatus.SUCCESS)
    def test_no_real_side_effects(self): self.assertFalse(hasattr(ActionGateway,"send"))

if __name__ == "__main__": unittest.main()
