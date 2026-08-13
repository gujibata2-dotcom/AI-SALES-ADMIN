# AI Customer Security

Tenant IDs are mandatory on customer-owned records. Cross-tenant employee access raises `TenantIsolationError`. Tool access requires both plan entitlement and employee permission. External content is data only; obvious attempts to override policy, authorization, secrets or billing are rejected by the lightweight guard.

This is a domain-layer control, not a claim of complete application security.
