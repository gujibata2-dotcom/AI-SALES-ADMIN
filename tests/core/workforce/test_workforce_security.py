import json
from pathlib import Path

ROOT = Path('app/api/core/workforce')

def test_schema_files_are_valid_json():
    for p in ROOT.rglob('*.schema.json'):
        data = json.loads(p.read_text())
        assert data.get('type') == 'object'
        assert data.get('additionalProperties') is False


def test_workforce_security_fixtures_block_unauthorized_coordination():
    expected = {'unauthorized-delegation','privilege-inheritance','unlimited-agents','team-permission-change','bypass-human-approval','audit-modification','infinite-workflow','infinite-delegation'}
    for p in Path('tests/core/workforce/security').glob('*.json'):
        data = json.loads(p.read_text())
        assert p.stem in expected
        assert data['expected'] == 'BLOCK' if 'infinite' not in p.stem else data['expected'] == 'STOP'


def test_parallel_execution_has_limits():
    data = json.loads(Path('tests/core/workforce/routing/parallel-limits.json').read_text())
    assert data['max_parallel_agents'] > 0
    assert data['max_workflow_depth'] > 0
    assert data['max_concurrent_tasks'] > 0


def test_conflict_requires_verified_source_or_human_review():
    data = json.loads(Path('tests/core/workforce/consensus/conflicting-price.json').read_text())
    assert data['resolution'] in {'VERIFIED_SOURCE','HUMAN_REVIEW'}
    assert data['majority_vote_is_sufficient'] is False
