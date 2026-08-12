"""Static Phase 33 validation; no network, credentials, or production calls."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMA_DIR=ROOT/'schemas'

def validate_json_schemas():
    errors=[]
    for p in sorted(SCHEMA_DIR.glob('*.schema.json')):
        try:
            data=json.loads(p.read_text())
            if data.get('$schema') is None: errors.append(f'{p}: missing $schema')
        except Exception as exc: errors.append(f'{p}: {exc}')
    return errors

if __name__=='__main__':
    errors=validate_json_schemas()
    print('PHASE33 STATIC SCHEMA CHECK')
    print('ERRORS',len(errors))
    for e in errors: print(e)
    raise SystemExit(1 if errors else 0)
