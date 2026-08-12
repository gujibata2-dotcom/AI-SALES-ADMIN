import unittest
from app.api.core.workforce.orchestration import choose_execution_mode, WorkforceMember, WorkforceStatus, eligible
from app.api.core.workforce.task_decomposition import validate_dag, ready_tasks
from app.api.core.workforce.handoff import validate_handoff, authorized_delegation
from app.api.core.workforce.conflict_resolution import resolve_strategy

class TestPhase33(unittest.TestCase):
    def test_single_agent_for_simple_task(self):
        self.assertEqual(choose_execution_mode(complexity=1,risk='LOW',required_capabilities=1).mode,'SINGLE_AGENT')
    def test_multi_agent_for_complex_task(self):
        self.assertEqual(choose_execution_mode(complexity=5,risk='MEDIUM',required_capabilities=3).mode,'MULTI_AGENT')
    def test_permission_boundary(self):
        m=WorkforceMember('e1','researcher',('research',),('read',),WorkforceStatus.AVAILABLE)
        self.assertFalse(eligible(m,{'research'},{'write'}))
    def test_dag_blocks_missing_dependency(self):
        self.assertFalse(validate_dag([{'task_id':'b','dependencies':['a']}])[0])
    def test_dag_rejects_cycle(self):
        self.assertFalse(validate_dag([{'task_id':'a','dependencies':['b']},{'task_id':'b','dependencies':['a']}])[0])
    def test_handoff_required_fields(self):
        self.assertFalse(validate_handoff({'objective':'x'})[0])
    def test_high_risk_delegation_requires_approval(self):
        self.assertFalse(authorized_delegation(scope={'read'},allowed={'read'},risk='HIGH'))
    def test_conflict_not_majority_vote(self):
        result=resolve_strategy([{'result':'A','evidence_quality':1,'confidence':.5},{'result':'B','evidence_quality':1,'confidence':.5}])
        self.assertEqual(result['status'],'ESCALATE')

if __name__=='__main__': unittest.main()
