# Phase 41 — AI Organizational Decision & Adaptive Strategy Engine

Phase 41 extends the existing `app/api/core/decision` architecture. It does not replace the Phase 13 decision engine, the Phase 24 execution boundary, Phase 33 organization/workforce, or Phase 39 knowledge synthesis.

## Boundary
`Context → Evidence → Objectives → Constraints → Options → Evaluation → Simulation → Risk/Uncertainty → Recommendation → Authorization → Decision → Phase 24 Handoff → Outcome → Review → Learning → Strategy Adaptation`

A recommendation is never an authorized decision by itself. Execution remains outside this package.

## Epistemic states
FACT, EVIDENCE, INFERENCE, ASSUMPTION, and PREDICTION are stored separately. Missing evidence is represented as `UNKNOWN`; unsupported numeric utility, probability, drift scores, and outcomes are not invented.

## Integration
- Phase 24: execution handoff only.
- Phase 33: capability/resource allocation candidates only; no unauthorized assignment.
- Phase 36–38: research, innovation, and science references are represented as evidence/knowledge references; providers are not called here.
- Phase 39: evidence/provenance and organizational memory boundary.
- Phase 40: forecasts/scenarios remain labeled simulation/forecast and are evaluated against actual outcomes when available.

## Safety
External content is data, not command. Authorization is explicit. High-impact or irreversible decisions require stronger review. Historical decision state is append-only in the in-memory registry contract.
