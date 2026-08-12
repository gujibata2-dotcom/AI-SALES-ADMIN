# Phase 1–6 Integration Baseline

## Purpose

This document establishes the integration boundary between the repository foundation and the Phase 7 Grounded Knowledge Retrieval Engine.

## Conversation Understanding output

Phase 6 must provide a normalized conversation state containing, at minimum:

- `customer_id_reference`: reference-only identifier; never real PII
- `language`
- `intent`
- `emotion`
- `context`
- `needs`
- `state`
- `output_constraints`

## Phase 7 input boundary

Retrieval consumes the semantic result of Phase 6 rather than raw customer text. Retrieval must preserve language and intent and must not introduce customer identity data into knowledge queries unless an explicitly authorized non-PII reference is required.

## Evidence boundary

Every factual answer generated from retrieved knowledge must be traceable to evidence containing:

- `source_id`
- `chunk_id`
- source status
- effective dates when applicable
- retrieval timestamp

## Trust boundary

The system must not treat missing, expired, archived, or conflicting knowledge as verified current fact. When evidence is insufficient, the response layer must communicate uncertainty or escalate rather than inventing information.

## Phase 7 implementation order

1. Define typed contracts.
2. Implement source eligibility filtering.
3. Implement chunk retrieval and ranking.
4. Attach evidence/provenance.
5. Resolve conflicts and insufficient evidence.
6. Add deterministic tests.
7. Connect the response layer only after retrieval tests pass.
