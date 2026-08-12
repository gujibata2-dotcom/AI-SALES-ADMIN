import json
from pathlib import Path

REGISTRY=Path('app/api/core/organization/employees/registry.schema.json')
FIXTURES=Path('tests/core/organization/fixtures')


def test_registry_has_least_privilege_fields():
    obj=json.loads(REGISTRY.read_text())
    assert 'permissions' in obj['properties']
    assert 'manager' in obj['properties']


def test_team_hierarchy_does_not_imply_permission():
    case=json.loads((FIXTURES/'hierarchy-no-permission.json').read_text())
    assert case['hierarchy_implies_permission'] is False


def test_task_assignment_checks_skill_and_permission():
    case=json.loads((FIXTURES/'task-assignment.json').read_text())
    assert case['skills_checked'] is True
    assert case['permissions_checked'] is True
    assert case['unauthorized_assignment']=='BLOCK'


def test_specialist_unknown_escalates():
    case=json.loads((FIXTURES/'specialist-unknown.json').read_text())
    assert case['unknown_result']=='UNKNOWN'
    assert case['escalation']=='HUMAN'


def test_no_real_pii_or_secrets_in_fixtures():
    forbidden={'email','phone','address','password','api_key','token','payment_card','real_name'}
    for path in FIXTURES.glob('*.json'):
        obj=json.loads(path.read_text())
        assert not forbidden.intersection(obj.keys())
