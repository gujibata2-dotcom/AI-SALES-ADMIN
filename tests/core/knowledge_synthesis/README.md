# Phase 39 validation

Dependency-light synthetic validation for schemas and core guardrails. Run from repository root:

`python -m json.tool app/api/core/knowledge_synthesis/schemas/knowledge.schema.json >/dev/null`

If pytest is available:

`python -m pytest tests/core/knowledge_synthesis -q`

Do not install dependencies from the network automatically. If a dependency is unavailable, report the limitation.