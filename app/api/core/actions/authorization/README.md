# Authorization

States: `AUTHORIZED`, `REQUIRES_APPROVAL`, `BLOCKED`, `EXPIRED`, `INVALID`.

Every action is checked before execution. AI cannot authorize itself. HIGH requires human approval. CRITICAL is BLOCKED in Phase 10.

Authorization is explicit, scoped, time-bounded, and never inferred from model output.