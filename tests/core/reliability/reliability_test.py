import unittest
from app.api.core.reliability.engine import *

class ReliabilityTests(unittest.TestCase):
    def test_unknown_without_evidence(self):
        r=HealthEngine.evaluate('x','QUEUE',[]); self.assertEqual(r.status,HealthStatus.UNKNOWN); self.assertIsNone(r.health_score)
    def test_healthy_with_evidence(self):
        r=HealthEngine.evaluate('x','QUEUE',[HealthCheck('availability',True,True)]); self.assertEqual(r.status,HealthStatus.HEALTHY)
    def test_correlation(self):
        c=AlertCorrelator(); a=c.correlate('api','gateway','timeout','i1'); b=c.correlate('api','gateway','timeout','i2'); self.assertEqual(a,b)
    def test_circuit_breaker(self):
        c=CircuitBreaker(2); c.failure(); c.failure(); self.assertEqual(c.state,CircuitState.OPEN); c.half_open(); self.assertEqual(c.state,CircuitState.HALF_OPEN); c.success(); self.assertEqual(c.state,CircuitState.CLOSED)
    def test_recovery_denied(self):
        i=Incident('i',IncidentSeverity.WARNING,'test',('x',),'failure','now'); p=RecoveryPolicy(('retry',),2,10,1,('x',))
        r=RecoveryEngine().recover(i,Diagnosis('timeout',EvidenceKind.OBSERVED,DiagnosisConfidence.HIGH,'timeout'),p,'retry',authorized=False); self.assertEqual(r.status,RecoveryStatus.STOPPED)
    def test_critical_security_escalates(self):
        i=Incident('i',IncidentSeverity.CRITICAL,'security',('x',),'breach','now'); p=RecoveryPolicy(('retry',),2,10,1,('x',))
        d=Diagnosis('security_incident',EvidenceKind.OBSERVED,DiagnosisConfidence.HIGH,'security event')
        r=RecoveryEngine().recover(i,d,p,'retry',authorized=True); self.assertEqual(r.status,RecoveryStatus.ESCALATED)
    def test_runaway(self):
        self.assertEqual(RunawayDetector().check(11,1,0,1,1,0,{'max_tasks':10}),'max_tasks')
    def test_dead_letter_preserves_context(self):
        q=DeadLetterQueue(); q.put({'task':'t'},'timeout',{'audit':'a'}); self.assertEqual(q.items[0]['context']['task'],'t')
    def test_kill_switch(self):
        k=KillSwitch(); k.stop('workflow:w'); self.assertTrue(k.is_stopped('workflow:w'))
    def test_security_guard(self):
        g=ReliabilityGuard(); self.assertFalse(g.allow('disable_kill_switch')); self.assertTrue(g.allow('retry'))

if __name__=='__main__': unittest.main()
