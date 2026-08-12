# Phase 7 Retrieval Acceptance Tests

- [ ] Verified active source is eligible for retrieval.
- [ ] Expired source is excluded from current factual claims.
- [ ] Archived source is excluded.
- [ ] Evidence includes `source_id` and `chunk_id`.
- [ ] Conflicting valid sources produce `conflict` state.
- [ ] Missing evidence produces `insufficient_evidence`.
- [ ] No fixture contains real customer identifiers or PII.
- [ ] Retrieval filters preserve language and intent from the Conversation Understanding layer.
- [ ] Current price/promotion/stock claims require valid effective dates.
- [ ] Response generation cannot silently replace missing evidence with invented facts.
