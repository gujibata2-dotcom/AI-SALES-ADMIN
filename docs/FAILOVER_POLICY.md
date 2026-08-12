# Failover Policy

Fallback providers/services must be approved in advance. On failure: detect → health-check approved fallback → authorize → switch → verify. The AI cannot select a new external provider or create new credentials.

Circuit breaker states: CLOSED → OPEN → HALF_OPEN → CLOSED. Resource pools remain isolated for Sales, Support, Content, Admin and Research so one workload cannot exhaust the organization.
