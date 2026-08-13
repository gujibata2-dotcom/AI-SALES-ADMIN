# AI Employee Runtime

The runtime exposes explicit lifecycle state and separates Plan, Authorize, Execute and Verify.

State progression for successful work is:
`RECEIVED → UNDERSTOOD → PLANNED → AUTHORIZED → RUNNING → VERIFYING → COMPLETED`.

Failure or uncertainty remains `FAILED`, `BLOCKED`, `UNKNOWN` or `REQUIRES_HUMAN`.

The reference runtime is intentionally provider-agnostic. It does not invent model, tool, payment or social-provider success.
