# Idempotency

Every side-effect-capable action requires an idempotency_key. Duplicate requests must not execute twice. Support duplicate detection, replay protection, and safe retry.
