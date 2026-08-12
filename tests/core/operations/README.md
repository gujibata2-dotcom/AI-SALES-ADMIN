# PHASE 24 — Autonomous Operations

Bounded autonomy control plane for AI Employees. The invariant is:

`Decision → Governance → Plan → Authorization → Action Gateway → Execution → Verification → Outcome → Learning`

## Safety invariants
- Default deny; no Agent may call an external adapter directly.
- L0/L5 and critical actions require human control.
- Permission, policy, risk, autonomy, scope, budget, rate, dependency and time limits are checked before execution.
- Idempotency prevents duplicate side effects.
- Verification is independent from transport/API success.
- UNKNOWN outcomes escalate according to risk.
- Rollback is recorded; irreversible actions use compensating actions and human escalation.
- Kill switch prevents new executions and supports safe shutdown.
- Audit records are append-only/immutable according to governance policy.

## Integrations
Facebook, Instagram, LINE, TikTok, Email, CRM, E-commerce and Payment are future adapters only. Production credentials, live publishing, messaging and transactions are intentionally not installed in Phase 24.
