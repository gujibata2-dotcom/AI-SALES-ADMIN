from app.api.core.organization.engine import StrategicAction, classify_status
from app.api.core.organization.governance import resolve_policy_conflict
from app.api.core.organization.risk import required_authority
from app.api.core.organization.scenario import scenario


def test_irreversible_requires_human():
    action = StrategicAction('org-test','publish', 'AI_AUTONOMOUS','IRREVERSIBLE',[{'source':'synthetic'}])
    assert 'irreversible action requires human governance' in action.validate()


def test_status_without_evidence_is_not_evaluated():
    assert classify_status(None, 10) == 'NOT_EVALUATED'


def test_critical_requires_human_only():
    assert required_authority('CRITICAL') == 'HUMAN_ONLY'


def test_policy_tie_escalates():
    result = resolve_policy_conflict([{'policy_id':'a','authority_rank':1},{'policy_id':'b','authority_rank':1}])
    assert result['status'] == 'ESCALATE'


def test_scenario_does_not_invent_probability():
    assert scenario('UNKNOWN', ['synthetic assumption'], 'unknown')['probability_if_known'] is None
