# Action Gateway

The Action Gateway is the only approved boundary for external side effects. Agents produce intent and requests; they never receive direct external API clients.

Pipeline: `Intent → Permission → Policy → Risk → Autonomy → Preflight → Gateway → Execute → Verify`.

Checks include authorization, scope, target, data classification, budget, rate limit, dependency state, timeout, approval requirements and idempotency. A failed check is a hard BLOCK.
