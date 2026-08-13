# AI Employee Service

Phase 45 exposes a customer-facing service boundary over the Phase 44 runtime. The service treats an AI Employee as a contracted organizational worker, not as a raw model.

## Lifecycle
Visitor → organization → trial → employee catalog → package → employee contract → use → usage/quota → performance → change/cancel.

`ServiceEngine` owns customer/organization records, subscriptions, employee contracts, usage metering, quota state, package entitlements and audit events. It reuses `app.api.core.production.runtime.TenantStore` and `Employee`.

No payment provider is implemented here. The default billing boundary returns `BILLING_NOT_CONFIGURED`; therefore no payment, invoice, renewal or commercial activation is claimed.
