# Error Handling

Error types: VALIDATION_ERROR, AUTHORIZATION_ERROR, TIMEOUT, RATE_LIMIT, NOT_FOUND, CONFLICT, PROVIDER_ERROR, UNKNOWN_ERROR.

Separate business errors from technical errors. Customer-facing output must not expose internal technical details, credentials, provider traces, or secrets.