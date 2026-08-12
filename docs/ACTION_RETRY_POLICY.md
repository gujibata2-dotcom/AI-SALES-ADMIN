# Retry Policy

Classify failures as RETRYABLE, NON_RETRYABLE, or UNKNOWN.

Retry metadata: max_attempts, backoff, reason, idempotency protection.

Never automatically retry payment or irreversible actions.