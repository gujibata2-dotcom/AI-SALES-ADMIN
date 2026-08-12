# Outbound Communication

Communication uses prepare → store outbound intent → authorize → queue → send → verify.

DRAFT and DRY_RUN never execute side effects. Idempotency keys prevent duplicate sends/posts. High-risk communications require configured human approval. Customer-facing sales gates include truth, product knowledge, privacy, ethics, authorization and platform policy.
