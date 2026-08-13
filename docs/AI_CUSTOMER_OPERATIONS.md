# AI Customer Operations

Execution records should carry tenant ID and correlation ID. Idempotency keys protect external actions from duplicate submission. Usage is recorded per tenant/resource. Recovery and durable persistence are integration responsibilities and must be evidenced before production readiness.

Social/product posting is represented as `NOT_CONNECTED` until a real adapter exists.
