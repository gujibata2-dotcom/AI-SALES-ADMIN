import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA_DIR=ROOT/'app'/'api'/'core'/'organization'/'schemas'
REQUIRED={'employee.schema.json','task.schema.json','capability.schema.json','role.schema.json','assignment.schema.json','dependency.schema.json','handoff.schema.json','agent-message.schema.json','team.schema.json','performance.schema.json','capability-gap.schema.json','organization-event.schema.json','quality-gate.schema.json','escalation.schema.json'}

def main():
    found={p.name for p in SCHEMA_DIR.glob('*.schema.json')}
    missing=REQUIRED-found
    if missing: raise SystemExit('missing schemas: '+', '.join(sorted(missing)))
    for p in SCHEMA_DIR.glob('*.schema.json'):
        json.loads(p.read_text(encoding='utf-8'))
    print('Phase 42 schema validation: OK')
if __name__=='__main__': main()
