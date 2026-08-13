"""Phase 46 static validation helper; no network or dependency installation."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/'app/api/core/workforce/schemas'
DOCS=[ROOT/'docs'/n for n in ('AI_WORKFORCE.md','AI_MULTI_AGENT_ORCHESTRATION.md','AI_EMPLOYEE_COLLABORATION.md','AI_WORKFORCE_SECURITY.md','AI_WORKFORCE_GOVERNANCE.md','AI_WORKFORCE_AUTONOMY.md')]

def main():
    files=list(SCHEMAS.glob('*.json'))
    assert len(files)==11, f'expected 11 Phase 46 schemas, got {len(files)}'
    for f in files: json.loads(f.read_text())
    assert all(p.exists() for p in DOCS)
    from app.api.core.workforce.workforce import WorkforceEngine
    e=WorkforceEngine(); e.create_workforce('CHECK','WF','FREE')
    assert e.workforces['CHECK:WF'].package_id=='FREE'
    print('PHASE46_STATIC_VALIDATION=PASS')

if __name__=='__main__': main()
