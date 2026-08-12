#!/usr/bin/env python3
"""Dependency-free Phase 36 validation: JSON validity + required structural checks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app/api/core/research/schemas"
REQUIRED = {
    "research-question.schema.json", "research-project.schema.json", "source.schema.json",
    "evidence.schema.json", "claim.schema.json", "hypothesis.schema.json", "experiment.schema.json",
    "research-finding.schema.json", "research-review.schema.json", "knowledge-gap.schema.json",
    "research-report.schema.json", "research-event.schema.json",
}

errors = []
files = {p.name for p in SCHEMA_DIR.glob("*.schema.json")}
missing = REQUIRED - files
if missing: errors.append(f"missing schemas: {sorted(missing)}")
for path in SCHEMA_DIR.glob("*.schema.json"):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"wrong schema dialect: {path.name}")
    except Exception as exc:
        errors.append(f"invalid JSON {path.name}: {exc}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    raise SystemExit(1)
print(f"PASS: {len(files)} Phase 36 schemas are valid JSON and use draft 2020-12")
