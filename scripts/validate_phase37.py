#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCHEMAS=ROOT/'app/api/core/innovation/schemas'
REQUIRED={'problem.schema.json','opportunity.schema.json','idea.schema.json','design.schema.json','prototype.schema.json','experiment.schema.json','invention.schema.json','innovation-review.schema.json','innovation-risk.schema.json','innovation-metric.schema.json','innovation-event.schema.json','ip-review.schema.json'}
errors=[]
files={p.name for p in SCHEMAS.glob('*.schema.json')}
errors += [f'missing schema: {x}' for x in sorted(REQUIRED-files)]
for p in SCHEMAS.glob('*.schema.json'):
    try:
        obj=json.loads(p.read_text(encoding='utf-8'))
        if obj.get('$schema')!='https://json-schema.org/draft/2020-12/schema': errors.append(f'wrong dialect: {p.name}')
    except Exception as e: errors.append(f'invalid JSON {p.name}: {e}')
if errors:
    print('FAIL'); print('\n'.join(errors)); raise SystemExit(1)
print(f'PASS: {len(files)} Phase 37 schemas are valid JSON')
