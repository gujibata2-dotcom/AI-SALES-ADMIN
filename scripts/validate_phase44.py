import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "app" / "api" / "core" / "production" / "schemas"
REQUIRED = {
    "employee-deployment.schema.json", "task-execution.schema.json",
    "employee-permission.schema.json", "customer-tenant.schema.json",
    "usage-quota.schema.json", "production-readiness.schema.json",
    "employee-performance.schema.json", "audit-event.schema.json",
    "execution-event.schema.json",
}

def main():
    found = {p.name for p in SCHEMA_DIR.glob("*.schema.json")}
    missing = REQUIRED - found
    if missing:
        raise SystemExit("missing schemas: " + ", ".join(sorted(missing)))
    for path in SCHEMA_DIR.glob("*.schema.json"):
        json.loads(path.read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT))
    suite = unittest.defaultTestLoader.loadTestsFromName("tests.core.production_test")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("Phase 44 validation: OK")

if __name__ == "__main__":
    main()
