"""Static Phase 38 validation without external dependencies."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
SCHEMA_DIR=ROOT/"app/api/core/science/schemas"
def validate_schemas():
    failures=[]
    for p in SCHEMA_DIR.glob("*.json"):
        try: json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc: failures.append((p.name,str(exc)))
    return failures
if __name__ == "__main__":
    failures=validate_schemas(); print("PASS" if not failures else failures); raise SystemExit(1 if failures else 0)
