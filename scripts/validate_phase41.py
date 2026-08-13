"""Static Phase 41 validation; standard library only.
Run from repository root: python scripts/validate_phase41.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app/api/core/decision/organizational/schemas"
REQUIRED_SCHEMAS = {
    "decision.schema.json", "objective.schema.json", "constraint.schema.json", "option.schema.json",
    "evaluation.schema.json", "tradeoff.schema.json", "authorization.schema.json", "outcome.schema.json",
    "strategy.schema.json", "goal.schema.json", "resource-allocation.schema.json", "decision-review.schema.json",
    "decision-version.schema.json", "decision-event.schema.json", "override.schema.json",
}
REQUIRED_BOUNDARIES = [
    "app/api/core/decision",
    "app/api/core/organization",
    "app/api/core/knowledge_synthesis",
    "app/api/core/release",
]

def main() -> int:
    errors = []
    for name in REQUIRED_SCHEMAS:
        path = SCHEMA_DIR / name
        if not path.exists(): errors.append(f"missing schema: {name}")
        else:
            try: json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc: errors.append(f"invalid JSON {name}: {exc}")
    for boundary in REQUIRED_BOUNDARIES:
        if not (ROOT / boundary).exists(): errors.append(f"missing integration boundary: {boundary}")
    if errors:
        for error in errors: print(error)
        return 1
    print(f"Phase 41 static validation OK: {len(REQUIRED_SCHEMAS)} schemas; compatibility boundaries present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
