# Phase 19 — Evaluation Engine

The Evaluation Engine is a production gate, not a learning mechanism. Learning recommendations from Phase 12 enter as candidates and must be evaluated before any behavior can be versioned or released.

Flow: Recommendation → Evaluation → Risk Assessment → Human Review → Approval/Rejection → Version → Canary → Monitor → Deploy/Rollback.

## Invariants
- LEARNING ≠ AUTOMATIC DEPLOYMENT.
- AI cannot approve, deploy, weaken safety gates, modify audit history, or bypass Action Gateway/governance.
- No source for a factual product claim means FAIL or REVIEW; model confidence is not evidence.
- Critical risk requires mandatory human approval.
- Regression in safety, ethics, privacy, accuracy, or customer experience blocks release.
- Evaluation data must be synthetic, approved historical, or human-reviewed; sensitive customer data requires authorization.

Evaluation types include response quality, knowledge accuracy, safety, ethics, sales quality, customer experience, multilingual, content quality, workflow, policy compliance, regression, security, and privacy.
