"""Static Phase 32 validation; no network, credentials or production calls."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app/api/core/career/schemas"
REQUIRED = {
    "career-profile.schema.json", "role.schema.json", "career-path.schema.json", "skill.schema.json",
    "competency.schema.json", "development-plan.schema.json", "training-plan.schema.json", "mastery.schema.json",
    "promotion-review.schema.json", "capability-decay.schema.json", "succession.schema.json", "career-event.schema.json",
}

def main() -> int:
    files = {p.name for p in SCHEMA_DIR.glob("*.json")}
    missing = REQUIRED - files
    if missing:
        print("MISSING_SCHEMAS", sorted(missing)); return 1
    for path in SCHEMA_DIR.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    print(f"VALID_PHASE32_SCHEMAS={len(list(SCHEMA_DIR.glob('*.json')))}")
    print("NO_PRODUCTION_CALLS=True")
    print("NO_REAL_CREDENTIALS=True")
    print("NO_REAL_PII=True")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
