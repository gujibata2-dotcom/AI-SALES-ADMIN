import unittest
from app.api.core.cognition.engine import *

class CognitiveSecurityTests(unittest.TestCase):
 def test_attention_relevance(self):
  e=AttentionEngine(); a=e.select('t','g',[AttentionItem('a',1,.9,1),AttentionItem('b',.1,1,1)]); self.assertEqual(a[0].item_id,'a')
 def test_working_memory_bounded(self):
  m=WorkingMemory(2); m.put({'x':1}); m.put({'x':2}); m.put({'x':3}); self.assertEqual(len(m.items),2)
 def test_unknown_stays_unknown(self): self.assertEqual(SelfEvaluator().calibrate(.9,0), 'UNKNOWN')
 def test_gap(self): self.assertEqual(GapDetector().detect('price','missing').topic,'price')
 def test_unverified_sources_review(self): self.assertEqual(SourceVerifier().verify([{'quality':'COMMUNITY','claim':'x'}]),KnowledgeStatus.PENDING_REVIEW)
 def test_learning_requires_governance(self):
  c=LearningCandidate('c','rule',('e',),{},.8,'LOW',True); self.assertFalse(LearningGate().approve(c,False,True))
 def test_goal_persistence(self): self.assertFalse(GoalPersistence('authorized').check('new mission'))
 def test_no_automatic_skill_promotion(self):
  s=Skill('s','sales'); self.assertEqual(SkillEvaluator().promote(s,{'sufficient':True}).lifecycle,'DISCOVERED')
 def test_security_candidate(self):
  c=LearningCandidate('c','permission_change',('e',),{},.9,'SECURITY',True); self.assertFalse(CognitiveEngine().safety_check(c))

if __name__=='__main__': unittest.main()
