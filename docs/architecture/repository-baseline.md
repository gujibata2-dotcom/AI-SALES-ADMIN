# Repository Baseline

The GitHub `main` branch currently contains only the initial repository marker. Phase 1–6 implementation files are therefore not assumed to exist in this repository until they are explicitly restored or recreated.

## Required top-level structure

```text
app/
components/
config/
data/
docs/
lib/
logs/
prompts/
scripts/
tests/
```

## Dependency order

```text
Phase 1 Foundation
  -> Phase 2 AI Employee Constitution
  -> Phase 3 Knowledge Engine Foundation
  -> Phase 4 Knowledge Trust / Update Policy
  -> Phase 5 Customer Response Pipeline
  -> Phase 6 Conversation Understanding
  -> Phase 7 Grounded Knowledge Retrieval
```

Phase 7 is allowed to define contracts and tests before the concrete Phase 1–6 implementation is restored. It must not fabricate upstream modules or silently bypass the Phase 6 boundary.

## Safety invariant

`customer_id_reference` is reference-only. Real customer identifiers, personal data, secrets, credentials, or production records must never appear in fixtures, examples, logs, or tests.
