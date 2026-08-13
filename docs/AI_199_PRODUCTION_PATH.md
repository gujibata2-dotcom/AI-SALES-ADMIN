# Phase 49 — 199 Production Path

This phase closes the application-level 199 execution path around the existing Phase 44/45 runtime. It does not claim that the deployed product is already production-ready.

## Flow

`Customer/Tenant → 199 Checkout → verified payment webhook → ACTIVE entitlement → Employee → Knowledge → authorized Task → Model → Verification → Result → Usage/Audit`

### Payment

The Stripe adapter creates a monthly subscription Checkout Session for `STARTER_199` at 199 THB. Stripe's current API uses minor units for two-decimal currencies, and THB is supported; therefore the request uses `19900` as the unit amount. urlStripe Checkout API referencehttps://docs.stripe.com/api/checkout/sessions/create urlStripe supported currencieshttps://docs.stripe.com/currencies

Activation is webhook-driven and signature-verified. A client redirect or self-reported payment cannot activate the entitlement.

### AI Employee

The gateway reuses the Phase 44 employee runtime and Phase 45 package/usage engine. It does not create a parallel employee executor. Employee activation requires permissions; task execution is tenant-scoped, authorized, quota-controlled, model-routed, verified and idempotent.

### Knowledge

Customer knowledge is stored under the tenant and injected as DATA ONLY into the model context. The system instructs the model to return `UNKNOWN` instead of inventing business facts.

### Result

A verified task result is stored and can only be retrieved by the owning tenant. Usage is metered once per idempotency key.

## Production gate

The repository currently reports `TESTABLE`, not `PRODUCTION_READY`, because the following require real deployment evidence:

- customer account/authentication and persistent session layer
- persistent production storage
- HTTPS webhook endpoint and real Stripe account configuration
- real model-provider credentials and successful live request
- monitoring and operational recovery evidence
- real end-to-end payment → execution → result test

Test adapters are explicitly `MOCKED` and do not count as live evidence.
