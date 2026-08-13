# Multi-Agent Orchestration

`WorkforceEngine` owns planning and coordination state. It does not duplicate Phase 44 execution. `execute()` constructs the existing runtime Task and delegates execution/verification to `EmployeeRuntime`.

Capability assignment requires evidence-backed capabilities and returns `NO_CAPABLE_EMPLOYEE` when no exact match exists. Dependencies are topologically ordered; independent tasks can be parallelized only when they do not share an executing employee.

Agent messages and handoffs are tenant-bound, provenance-bearing, and treated as data. Independent review is required; disagreement is not resolved by majority vote.
