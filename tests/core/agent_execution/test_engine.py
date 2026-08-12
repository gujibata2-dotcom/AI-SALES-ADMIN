import unittest
from app.api.core.agent_execution.engine import AgentSpec, ToolSpec, AgentTask, Risk, Status, AuthorizationGate, ExecutionController, DryRun

class Phase27SecurityTests(unittest.TestCase):
    def setUp(self):
        self.tool=ToolSpec('send','send','message','COMMUNICATE',{}, {}, Risk.HIGH,'send.customer',False,True,Status.ACTIVE)
        self.task=AgentTask('t1','employee','agent','objective',{}, {}, ('send',), {}, Risk.HIGH,None,10, {})
    def test_high_risk_requires_human_approval(self):
        gate=AuthorizationGate({'send'},{'send'},{'send.customer'},False)
        self.assertFalse(gate.authorize(self.task,self.tool))
    def test_blocked_tool_denied(self):
        blocked=ToolSpec('x','x','x','READ',{}, {}, Risk.LOW,'read',True,False,Status.BLOCKED)
        gate=AuthorizationGate({'x'},{'x'},{'read'},True)
        self.assertFalse(gate.authorize(self.task,blocked))
    def test_retry_only_transient(self):
        c=ExecutionController(max_retries=2)
        self.assertTrue(c.retryable('TIMEOUT')); self.assertFalse(c.retryable('AUTHORIZATION_FAILURE'))
    def test_step_limit(self):
        c=ExecutionController(max_steps=1)
        actions=[]
        from app.api.core.agent_execution.engine import Action
        actions=[Action('a','t','x','agent','op',{}, {}, Risk.LOW)]*2
        ok,reason=c.preflight(self.task,actions)
        self.assertFalse(ok); self.assertEqual(reason,'MAX_STEPS_EXCEEDED')
    def test_dry_run_has_no_side_effect(self):
        from app.api.core.agent_execution.engine import Action
        action=Action('a','t','send','agent','send',{'x':'y'},{},Risk.HIGH)
        out=DryRun().plan([action])[0]
        self.assertFalse(out['external_side_effect'])

if __name__ == '__main__': unittest.main()
