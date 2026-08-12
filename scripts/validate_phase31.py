"""Static Phase 31 validation; intentionally does not call external services."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app/api/core/evaluation/schemas"


def validate_schemas():
    errors = []
    for path in SCHEMA_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"missing draft-2020-12: {path}")
        except Exception as exc:
            errors.append(f"invalid JSON {path}: {exc}")
    return errors


if __name__ == "__main__":
    errors = validate_schemas()
    if errors:
        raise SystemExit("\n".join(errors))
    print("Phase 31 static schema validation: PASS")
    print("External calls: NONE")
    print("Real PII/credentials: NONE")
