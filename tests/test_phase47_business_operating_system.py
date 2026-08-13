import unittest
from app.api.core.business_operating_system.engine import BusinessOperatingSystem, GoalStatus, Trigger, WorkflowState, TransitionError, AuthorizationError

class Phase47Tests(unittest.TestCase):
 def setUp(self): self.b=BusinessOperatingSystem(); self.g=self.b.create_goal("org-1",title="Increase sales",description="verified target",domain="sales",priority=1,target=10,metric="qualified_leads",deadline=None,owner="human")
 def process(self): return self.b.create_process(name="lead flow",purpose="qualify leads",trigger=Trigger.EVENT,inputs=("lead",),outputs=("qualified",),steps=("qualify","followup"),dependencies=(),owners=("sales",),risk_level="LOW")
 def test_goal_and_workflow(self):
  self.assertEqual(self.b.approve_goal(self.g.goal_id,"human").status,GoalStatus.APPROVED); p=self.process(); w=self.b.create_workflow("org-1",self.g.goal_id,p.process_id,"human",authorized=True); self.b.transition(w.workflow_id,WorkflowState.QUEUED); self.b.transition(w.workflow_id,WorkflowState.RUNNING); self.assertEqual(w.state,WorkflowState.RUNNING)
 def test_invalid_transition(self):
  p=self.process(); w=self.b.create_workflow("org-1",self.g.goal_id,p.process_id,"human",authorized=True)
  with self.assertRaises(TransitionError): self.b.transition(w.workflow_id,WorkflowState.COMPLETED)
 def test_pause_resume_and_idempotency(self):
  p=self.process(); w=self.b.create_workflow("org-1",self.g.goal_id,p.process_id,"human",authorized=True); self.b.transition(w.workflow_id,WorkflowState.QUEUED); self.b.transition(w.workflow_id,WorkflowState.RUNNING); self.b.pause(w.workflow_id,"human"); self.b.resume(w.workflow_id,"human"); self.assertTrue(self.b.execute_gate(w.workflow_id,"send","human",True,idempotency_key="k")); self.assertFalse(self.b.execute_gate(w.workflow_id,"send","human",True,idempotency_key="k"))
 def test_security_and_stop(self):
  p=self.process(); w=self.b.create_workflow("org-1",self.g.goal_id,p.process_id,"human",authorized=True)
  with self.assertRaises(AuthorizationError): self.b.execute_gate(w.workflow_id,"send","human",False)
  self.b.emergency_stop(w.workflow_id,"human","manual stop","org-1")
  with self.assertRaises(AuthorizationError): self.b.execute_gate(w.workflow_id,"send","human",True)
 def test_deadlock_roi_and_no_fake_data(self):
  self.assertTrue(self.b.detect_deadlock({"A":{"B"},"B":{"C"},"C":{"A"}})); self.assertFalse(self.b.detect_deadlock({"A":{"B"},"B":set()})); self.assertEqual(self.b.roi(None,None,None,None)["status"],"INSUFFICIENT_DATA"); self.assertEqual(self.b.business_health()["status"],"NO_DATA")
 def test_outcome_separation(self):
  p=self.process(); w=self.b.create_workflow("org-1",self.g.goal_id,p.process_id,"human",authorized=True); t=self.b.record_outcome(w.workflow_id,"TASK_OUTCOME","SUCCESS","execution evidence","task"); b=self.b.record_outcome(w.workflow_id,"BUSINESS_OUTCOME","NOT_ACHIEVED","no purchase evidence","crm"); self.assertNotEqual(t.kind,b.kind)

if __name__=="__main__": unittest.main()
