import unittest
from app.api.core.integrations.engine import ExternalSystem, OutboundIntent, Operation, Risk, IntegrationGate, WebhookEvent, WebhookVerifier, Outbox, RateLimiter, BudgetGuard, DraftMode

class Phase28SecurityTests(unittest.TestCase):
    def setUp(self):
        self.system=ExternalSystem('mock-line','Mock LINE','mock','messaging',('messaging','webhooks'),'MOCK',allowed_operations=('READ','SEND'),requires_human_approval=False,rate_limits={'SEND':2},webhook_support=True)
    def intent(self, op=Operation.SEND, risk=Risk.LOW, key='k1'):
        return OutboundIntent('r1','a1',key,'mock-line',op,{'text':'fixture'},'customer_id_reference',risk)
    def test_unauthorized_send_blocked(self):
        gate=IntegrationGate({'READ'},{'SEND'})
        self.assertFalse(gate.authorize(self.intent(),self.system)[0])
    def test_publish_unsupported_blocked(self):
        gate=IntegrationGate({'PUBLISH'},{'PUBLISH'})
        self.assertFalse(gate.authorize(self.intent(Operation.PUBLISH),self.system)[0])
    def test_high_risk_requires_approval(self):
        gate=IntegrationGate({'SEND'},{'SEND'},human_approval=False)
        self.assertFalse(gate.authorize(self.intent(risk=Risk.HIGH),self.system)[0])
    def test_duplicate_outbox_blocked(self):
        outbox=Outbox(); self.assertTrue(outbox.put(self.intent())); self.assertFalse(outbox.put(self.intent(key='k1')))
    def test_webhook_signature_replay_and_age(self):
        v=WebhookVerifier(300); seen=set(); e=WebhookEvent('e1','mock','message',1000,'sig','payload')
        self.assertTrue(v.verify(e,1000,'sig',seen)[0]); self.assertFalse(v.verify(e,1000,'sig',seen)[0])
        old=WebhookEvent('e2','mock','message',0,'sig','payload'); self.assertFalse(v.verify(old,1000,'sig',seen)[0])
        bad=WebhookEvent('e3','mock','message',1000,'bad','payload'); self.assertFalse(v.verify(bad,1000,'sig',seen)[0])
    def test_rate_limit(self):
        r=RateLimiter({'SEND':2}); self.assertTrue(r.allow('SEND')); self.assertTrue(r.allow('SEND')); self.assertFalse(r.allow('SEND'))
    def test_budget(self):
        b=BudgetGuard(daily=10,monthly=20); self.assertTrue(b.allow(5,10,5)); self.assertFalse(b.allow(8,10,5))
    def test_draft_has_no_side_effect(self):
        d=DraftMode().prepare(self.intent()); self.assertFalse(d['expected_side_effect']); self.assertEqual(d['status'],'DRAFT')

if __name__=='__main__': unittest.main()
