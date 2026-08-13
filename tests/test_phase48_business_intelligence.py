import unittest
from app.api.core.business_intelligence import BusinessIntelligence,Evidence,DecisionOption,DecisionAuthorizationError
class Phase48Tests(unittest.TestCase):
 def setUp(self): self.bi=BusinessIntelligence()
 def test_event_metric_state(self):
  e=self.bi.event('t1','sale','crm','lead',{'amount':10},1.0,{'source_id':'x'}); self.assertEqual(e.tenant_id,'t1')
  m=self.bi.metric('sales',10,'THB','day','crm','sum verified sales',1); self.assertEqual(m.evidence,Evidence.FACT)
  self.assertEqual(self.bi.state('o').status.value,'UNKNOWN')
 def test_signal_anomaly_trend(self):
  self.assertEqual(self.bi.anomaly('sales_drop',[1,2]).details['status'],'UNKNOWN'); self.assertEqual(self.bi.trend([1,2],'day')['direction'],'UNKNOWN')
 def test_decision_requires_evidence_and_approval(self):
  o=DecisionOption('a','A',100,20,10,1,{},[],5,{},'REVERSIBLE'); d=self.bi.decision('g','p',{},[o]);
  with self.assertRaises(ValueError): self.bi.recommend(d.decision_id,[])
  self.bi.recommend(d.decision_id,['metric:sales']);
  with self.assertRaises(DecisionAuthorizationError): self.bi.approve(d.decision_id,'ai','HIGH',False)
 def test_forecast_simulation_and_effectiveness(self):
  self.assertEqual(self.bi.forecast('sales',[1,2,3],'7d',{},.2).status,'FORECAST_UNAVAILABLE'); self.assertEqual(self.bi.simulation({}, {}, {}, {})['type'],'SIMULATION'); self.assertEqual(self.bi.effectiveness('d',10,12)['prediction_error'],2)
 def test_disagreement_and_override(self):
  o=DecisionOption('a','A',1,0,0,1,{},[],0,{},'REVERSIBLE'); d=self.bi.decision('g','p',{},[o]); self.bi.recommend(d.decision_id,['e']); self.bi.approve(d.decision_id,'human','HIGH',True); r=self.bi.override(d.decision_id,'human','reason','B'); self.assertEqual(r['new_decision'],'B'); self.assertEqual(self.bi.disagreement([{'recommendation':'A'},{'recommendation':'B'}]),'DISAGREEMENT')
if __name__=='__main__': unittest.main()
