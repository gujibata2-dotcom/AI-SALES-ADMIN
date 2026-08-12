# Action Integration

Customer-facing side effects always use: LLM → Decision → Orchestration → Action Gateway → Channel Adapter → Customer. Channel adapters never send directly from an LLM and never bypass Phase 14 authorization/policy/idempotency/verification.