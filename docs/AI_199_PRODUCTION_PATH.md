# Phase 49 — Closing the 199 Customer Path

## Authoritative path

Customer → 199 Checkout → verified payment webhook → ACTIVE entitlement → AI Employee → customer knowledge → authorized task → model provider → verification → result → usage/audit.

The implementation reuses Phase 44 production runtime and Phase 45 service/package/usage primitives rather than creating a second employee engine.

## What is real

- `STARTER_199` exists as a configurable package in Phase 45.
- Employee limits and package feature checks are server-side.
- Tenant-scoped knowledge is passed to the employee as data context.
- Tasks use Phase 44 authorization, quota, kill-switch, model routing, verification and idempotency.
- Results are tenant-checked before retrieval.
- Payment activation occurs only from a verified provider webhook; a browser/client claim cannot activate the plan.
- Stripe Checkout is implemented with Python stdlib HTTP and requires `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET`.
- An OpenAI-compatible model adapter is implemented with stdlib HTTP and requires `MODEL_API_KEY` and `MODEL_NAME` (and optionally `MODEL_API_BASE`).

## Important production boundary

The repository cannot honestly claim that money can be accepted today merely because the adapter exists. A real payment account, webhook endpoint, HTTPS deployment, secrets, database persistence and a real model provider must be configured and exercised in the deployed environment.

`Mocked` providers are test-only and never count as live readiness evidence.

## Activation sequence

1. Create tenant and start the 199 checkout session.
2. Customer completes checkout.
3. Provider webhook is verified and the local subscription becomes `ACTIVE`.
4. Customer creates a Sales/Support/Content employee within the package limit.
5. Employee is activated only with the required permissions.
6. Customer imports knowledge.
7. Customer submits an idempotent task.
8. Runtime authorizes and executes through the configured model provider.
9. Output is verified and stored with tenant-scoped result access.
10. Usage and audit events are recorded.

## Remaining deployment evidence

Before calling 199 `PRODUCTION_READY`, run the full E2E against a real payment sandbox/live configuration and a real model provider, plus tenant-isolation, security, recovery and monitoring checks. The readiness object remains `TESTABLE` until both payment and model adapters report live connectivity.
