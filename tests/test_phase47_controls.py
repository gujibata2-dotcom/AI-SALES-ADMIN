import unittest
from app.api.core.business_operating_system.controls import RetryPolicy,SLA,WorkflowControls
class Phase47ControlTests(unittest.TestCase):
 def test_retry_blocks_destructive_without_idempotency(self):
  p=RetryPolicy(3,1.0,frozenset({'TIMEOUT'}),frozenset({'PERMISSION'})); self.assertFalse(p.allowed('TIMEOUT',0,destructive=True,idempotent=False)); self.assertTrue(p.allowed('TIMEOUT',0,destructive=True,idempotent=True))
 def test_sla_and_fallback(self):
  c=WorkflowControls(); c.register_sla(SLA('s',100,'HIGH')); self.assertEqual(c.sla_status('s',50).status,'ON_TRACK'); r=c.fallback('A','B',{'sales'},{'SEND' },'LOW',{'sales'},{'SEND'}); self.assertEqual(r.action,'FALLBACK')
 def test_experiment_needs_evidence(self):
  c=WorkflowControls(); c.experiment('e','h','conversion','10%','7d','higher'); c.conclude_experiment('e',{'delta':1},'MEASURED'); self.assertEqual(c.experiments['e']['evidence'],'MEASURED')
if __name__=='__main__': unittest.main()
