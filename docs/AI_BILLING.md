# AI Billing

Billing is deliberately separated from plan and entitlement definitions. The current Phase 49 provider boundary returns `PAYMENT_NOT_CONNECTED`; it never fabricates a transaction, invoice or paid subscription.

Card numbers, CVV and payment secrets are outside the product domain and must never be stored here.
