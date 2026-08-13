import unittest
from app.api.core.business_intelligence.engine import BusinessIntelligence,DecisionOption,Assumption,Evidence,DecisionStatus,DecisionAuthorizationError

class Phase48Tests(unittest.TestCase):
 def setUp(self): self.b=BusinessIntelligence()
 def opts(self): return [DecisionOption('a','OPTION_A',100,20,10,2,1,(),5,{},'REVERSIBLE'),DecisionOption('b','OPTION_B',80,10,5,3,1,(),3,{},'PARTIALLY_REVERSIBLE')]
 def test_state_signal_anomaly_trend(self):
  s=self.b.state('org'); self.assertEqual(s.status.value,'UNKNOWN'); self.b.signal('sales_drop','crm',.8,Evidence.FACT); self.assertEqual(self.b.trend([1,2,3,4],'7d')['trend'],'upward'); self.assertIn('ANOMALY',self.b.anomaly('sales',[1,1,1,2],1).status)
 def test_decision_options_tradeoff_and_approval(self):
  d=self.b.create_decision('sales',{},'conversion decline',self.opts()); self.b.recommend(d.decision_id,[{'source':'crm'}],'MEDIUM'); self.assertEqual(d.status,DecisionStatus.REVIEW_REQUIRED); self.assertEqual(self.b.compare(d.decision_id)[0]['option'],'OPTION_A')
  with self.assertRaises(DecisionAuthorizationError): self.b.approve(d.decision_id,'ai','HIGH',False)
  self.b.approve(d.decision_id,'human','HIGH',True); self.assertEqual(d.status,DecisionStatus.APPROVED)
 def test_simulation_forecast_risk_opportunity(self):
  self.assertEqual(self.b.what_if('price changes')['evidence'],'SIMULATION'); self.assertEqual(self.b.counterfactual('no action')['type'],'SIMULATION'); self.assertEqual(self.b.forecast('sales',[1,2,3],'7d',{}).evidence,Evidence.UNKNOWN); self.assertEqual(self.b.risk('x',None,None,'UNKNOWN',{},None,None).severity,'UNKNOWN'); self.assertEqual(self.b.opportunity('cost','x',{},10,2,1,.7).confidence,.7)
 def test_override_journal_effectiveness_and_disagreement(self):
  d=self.b.create_decision('g',{},'p',self.opts()); r=self.b.override(d.decision_id,'human','changed context','OPTION_B'); self.assertEqual(r['new_decision'],'OPTION_B'); self.b.journal_entry(d.decision_id,{},'r',[],[],[],True,True,{},'lesson'); self.assertEqual(self.b.effectiveness(100,90)['error'],-10); self.assertFalse(self.b.disagreement([{'agent':'A'}])['majority_vote'])
 def test_security_privacy_boundary(self):
  d=self.b.create_decision('g',{},'p',self.opts());
  with self.assertRaises(DecisionAuthorizationError): self.b.approve(d.decision_id,'actor','CRITICAL',False)
  self.assertEqual(self.b.knowledge_trace('k','fresh','source',.8,'org')['scope'],'org')
if __name__=='__main__': unittest.main()
