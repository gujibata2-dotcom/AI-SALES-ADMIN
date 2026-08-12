# Failure isolation and circuit breaker

Agent/service failure: detect → pause affected task → isolate fault → bounded retry → backup or escalation.

Retry limits are finite. No infinite retry, delegation, or workflow.

Circuit breaker states: CLOSED → OPEN when failures exceed threshold → WAIT → TEST → CLOSED when healthy. While OPEN, stop new requests to the failing dependency.