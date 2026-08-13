# Runtime, security and verification

The runtime treats external data as untrusted data. Product descriptions, comments and links are not executable instructions.

Controls covered by the reference implementation include tenant isolation, least-privilege action authorization, idempotency, quota enforcement, kill switches, audit events, model configuration checks and outcome verification.

A failed verifier produces `UNKNOWN`, not `COMPLETED`. A missing provider/model produces `UNKNOWN`/`NOT_CONFIGURED`; a missing permission produces `REQUIRES_HUMAN`.
