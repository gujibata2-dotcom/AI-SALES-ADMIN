import json
from pathlib import Path

IDENTITY=Path('app/api/core/employee/identity/employee.schema.json')
MESSAGE=Path('app/api/core/organization/collaboration/message.schema.json')
REGISTRY=Path('app/api/core/organization/employees/registry.schema.json')
FIXTURES=Path('tests/core/employee/fixtures')


def schema(path, required):
    obj=json.loads(path.read_text())
    assert obj['type']=='object'
    assert set(obj['required'])==set(required)
    return obj


def test_employee_identity_schema():
    schema(IDENTITY,['employee_id','employee_type','display_name','role','department','status','manager_reference','created_at','version','capabilities','permission_profile'])


def test_collaboration_schema():
    schema(MESSAGE,['message_id','sender_employee_id','receiver_employee_id','task_id','message_type','payload','timestamp','correlation_id'])


def test_registry_schema():
    schema(REGISTRY,['employee_id','name','type','role','department','skills','permissions','manager','status','version','created_at'])


def test_security_fixtures_block_self_privilege_and_bypass():
    for name in ['self-create-admin','self-grant-permission','create-unrestricted-agent','self-approve','delete-audit','bypass-governance','permission-propagation']:
        assert json.loads((FIXTURES/f'{name}.json').read_text())['expected']=='BLOCK'


def test_delegation_uses_executor_permissions():
    case=json.loads((FIXTURES/'delegation-permission.json').read_text())
    assert case['expected_permission_source']=='executor'
    assert case['propagate_sender_permission'] is False


def test_lifecycle_preserves_audit():
    case=json.loads((FIXTURES/'retirement.json').read_text())
    assert case['history_preserved'] is True
    assert case['audit_preserved'] is True
