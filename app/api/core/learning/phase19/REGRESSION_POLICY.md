# Phase 19 Regression & Rollback Policy

A candidate improvement may be promoted only when evaluation and canary evidence do not violate configured regression thresholds.

## Required signals

- quality / correctness
- task success
- sales outcome where applicable
- customer satisfaction / negative feedback
- safety and policy violations
- retrieval quality
- workflow failure rate
- latency and reliability

## Rollback rules

Rollback is mandatory when a monitored candidate produces a material regression against the approved baseline, violates a safety/policy invariant, or becomes operationally unhealthy.

Rollback must:

1. stop further promotion;
2. restore the last known-good version;
3. record the reason and evidence;
4. preserve the candidate for investigation;
5. emit a new learning event so the failure enters the next cycle.

The learning engine must never suppress, rewrite, or delete regression evidence in order to make a candidate appear successful.
