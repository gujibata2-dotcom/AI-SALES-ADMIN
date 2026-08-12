# Phase 7 — Grounded Knowledge Retrieval Engine

## Objective
Build a retrieval layer that answers from verified product/business knowledge instead of guessing.

## Scope
- Knowledge source contracts
- Document/chunk normalization metadata
- Retrieval request/response contracts
- Trust and provenance requirements
- Citation-ready evidence records
- Test fixtures with synthetic data only

## Non-goals
- No external vector database yet
- No production LLM provider integration yet
- No customer PII in fixtures, logs, prompts, or examples
- No autonomous knowledge publishing without verification

## Pipeline
`source -> ingest -> normalize -> chunk -> index -> retrieve -> rerank -> evidence -> response`

Every answer produced from knowledge must be traceable to evidence with a stable `source_id` and `chunk_id`.
