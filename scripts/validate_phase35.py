import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app" / "api" / "core" / "economy" / "schemas"
REQUIRED = {"resource.schema.json","cost.schema.json","budget.schema.json","allocation.schema.json","capacity.schema.json","value.schema.json","roi.schema.json","investment.schema.json","forecast.schema.json","scenario.schema.json","economic-alert.schema.json","economic-event.schema.json","model-economics.schema.json","tool-economics.schema.json"}

def main():
    actual = {p.name for p in SCHEMA_DIR.glob("*.json")}
    missing = REQUIRED - actual
    for p in SCHEMA_DIR.glob("*.json"):
        json.loads(p.read_text(encoding="utf-8"))
    if missing:
        raise SystemExit(f"missing schemas: {sorted(missing)}")
    print(f"validated {len(actual)} Phase 35 schemas")

if __name__ == "__main__":
    main()
