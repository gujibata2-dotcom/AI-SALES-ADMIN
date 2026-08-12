# Execution Engine

Execution accepts only an authorized action, validates parameters, invokes an adapter, captures a structured result, verifies the result, and returns output.

BLOCKED, EXPIRED, or UNAUTHORIZED actions must never execute. Phase 10 adapters are mocks only; there are no external side effects.