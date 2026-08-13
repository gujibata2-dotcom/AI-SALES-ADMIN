"""Static Phase 41 contract validation using only the Python standard library."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
SCHEMA_DIR = ROOT / "schemas"

def main():
    errors=[]
    files=sorted(SCHEMA_DIR.glob("*.schema.json"))
    for path in files:
        try:
            data=json.loads(path.read_text(encoding="utf-8"))
            if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema": errors.append(f"{path}: wrong $schema")
            if not data.get("$id"): errors.append(f"{path}: missing $id")
            if data.get("type") != "object": errors.append(f"{path}: root must be object")
        except Exception as exc: errors.append(f"{path}: {exc}")
    if errors:
        for error in errors: print(error)
        return 1
    print(f"Validated {len(files)} Phase 41 schemas")
    return 0

if __name__ == "__main__": sys.exit(main())
