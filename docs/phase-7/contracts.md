# Phase 7 Contracts

## Knowledge document

Required fields:
- `source_id`: stable non-PII identifier
- `title`: human-readable source title
- `source_type`: product | policy | faq | promotion | catalog | other
- `content`: normalized source text
- `version`: source version
- `status`: draft | verified | expired | archived
- `verified_at`: timestamp or null
- `verified_by`: system/role identifier or null
- `effective_from`: timestamp or null
- `effective_until`: timestamp or null

## Retrieval request

```text
query: string
language: string | null
customer_context: non-sensitive structured context only
filters: source_type/status/effective-date filters
limit: integer
```

## Evidence record

```text
source_id: string
chunk_id: string
score: number
content: string
source_version: string
verified: boolean
valid_now: boolean
```

## Trust rules

1. Prefer verified sources over unverified sources.
2. Never use expired knowledge for current price, promotion, stock, policy, or availability claims.
3. If evidence conflicts, prefer the newest valid verified version and mark the conflict for review.
4. If no sufficiently trusted evidence exists, the agent must not invent an answer.
5. Customer PII must never be used as a retrieval key or written into evidence fixtures/logs.
6. Every grounded claim must remain traceable to source and chunk identifiers.
