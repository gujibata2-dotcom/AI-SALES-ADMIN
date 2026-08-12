import json
from pathlib import Path

SCHEMA = Path('app/api/core/evaluation/output/evaluation.schema.json')
FIXTURES = Path('tests/core/evaluation/fixtures')

REQUIRED = {'evaluation_id','candidate_id','version','evaluation_type','dataset_reference','criteria','scores','failures','warnings','risk_level','recommendation','review_required','created_at'}


def test_evaluation_schema_is_valid_json():
    schema = json.loads(SCHEMA.read_text())
    assert schema['type'] == 'object'
    assert set(schema['required']) == REQUIRED


def test_synthetic_fixtures_are_json_and_have_no_customer_pii_fields():
    forbidden = {'email','phone','address','customer_id','real_name','payment_card'}
    for path in FIXTURES.glob('*.json'):
        payload = json.loads(path.read_text())
        assert not forbidden.intersection(payload.keys())


def test_governance_attacks_are_blocked():
    for name in ('self-approve','self-deploy','disable-safety','modify-audit','bypass-canary','bypass-rollback'):
        payload = json.loads((FIXTURES / f'{name}.json').read_text())
        assert payload['expected'] == 'BLOCK'


def test_critical_requires_human_approval():
    payload = json.loads((FIXTURES / 'critical-change.json').read_text())
    assert payload['risk_level'] == 'CRITICAL'
    assert payload['human_approval_required'] is True


def test_multilingual_cases_are_semantically_consistent():
    payload = json.loads((FIXTURES / 'multilingual-consistency.json').read_text())
    assert payload['factual_meaning_consistent'] is True
    assert payload['languages'] == ['th','en','zh','ja','ko']
