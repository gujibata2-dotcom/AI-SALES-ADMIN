"""Static Phase 34 validation; no network, secrets, or production calls."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / 'schemas'
EXPECTED = ['organization.schema.json','mission.schema.json','goal.schema.json','objective.schema.json','strategy.schema.json','decision.schema.json','policy.schema.json','risk.schema.json','resource-allocation.schema.json','portfolio.schema.json','scenario.schema.json','performance.schema.json','incident.schema.json','organization-event.schema.json']

def main():
    missing=[]
    for name in EXPECTED:
        p=SCHEMA_DIR/name
        if not p.exists(): missing.append(name); continue
        json.loads(p.read_text(encoding='utf-8'))
    if missing: raise SystemExit(f'MISSING: {missing}')
    print(f'Phase 34 static validation: {len(EXPECTED)} schemas valid')
    print('No real data, credentials, external calls, or fake performance evidence used.')

if __name__ == '__main__': main()
