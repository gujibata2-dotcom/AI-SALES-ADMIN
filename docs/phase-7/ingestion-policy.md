# Phase 7 — Knowledge Ingestion Policy

## Pipeline

`document → validation → normalization → chunking → provenance → retrieval`

## Rules

1. Every document requires a stable `source_id`.
2. Empty documents are rejected.
3. Whitespace and line endings are normalized deterministically.
4. Language is normalized to lowercase.
5. Chunks retain source, language, status, effective dates, and source URI.
6. Chunk IDs are deterministic: `<source_id>:<sequence>`.
7. Ingestion never changes the truth of source content.
8. Production PII, credentials, tokens, and secrets are prohibited in fixtures and examples.
9. Retrieval remains responsible for deciding whether a chunk is eligible as-of a requested date.
