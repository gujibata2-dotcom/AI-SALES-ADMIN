# AI Employee Billing

Billing is an abstraction only. The default `BillingProvider` has `configured = False` and returns `BILLING_NOT_CONFIGURED` for subscription creation/cancellation.

No card number, CVV, raw payment credential or secret is stored. A real provider adapter must supply provider references and independently verify webhook signatures, event IDs, timestamps and replay/idempotency before changing subscription state.
