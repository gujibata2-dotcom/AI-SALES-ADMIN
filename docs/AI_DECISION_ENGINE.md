# Phase 41 — AI Decision Engine

Phase 41 defines decision support as a controlled pipeline: Situation → Context → Evidence → Objectives → Constraints → Options → Evaluation → Simulation → Risk/Uncertainty → Recommendation → Authorization → Phase 24 handoff → Outcome → Review → Learning → Adaptation.

## Boundary
Intelligence is not a decision. A recommendation is not authorization. The engine never executes an action directly. Authorized decisions are handed to the Phase 24 execution boundary.

## Evidence discipline
Objects preserve FACT/EVIDENCE/INFERENCE/ASSUMPTION/PREDICTION/OPTION/RECOMMENDATION/DECISION/ACTION/OUTCOME/LESSON as separate concepts. Missing evidence is represented as UNKNOWN or DO_NOT_KNOW; probabilities and numeric utility are not invented.

## Decision quality
Reviews distinguish decision quality from outcome quality: GOOD_DECISION_GOOD_OUTCOME, GOOD_DECISION_BAD_OUTCOME, BAD_DECISION_GOOD_OUTCOME, BAD_DECISION_BAD_OUTCOME, and INSUFFICIENT_EVIDENCE. Original context, evidence, assumptions and forecast are versioned to resist hindsight bias.

## Strategy adaptation
Strategies are versioned and can move through DRAFT, PROPOSED, REVIEW, APPROVED, ACTIVE, PAUSED, ADAPTING, SUPERSEDED and RETIRED. Adaptation requires a trigger and evidence references.

## Integrations
Phase 36 research resolves knowledge gaps; Phase 37 experiments inform options; Phase 38 scientific findings can become evidence; Phase 39 supplies verified knowledge; Phase 40 supplies forecasts/scenarios. Phase 26/33 provide capability and workforce candidates, Phase 34 provides organizational goals/governance, Phase 35 provides resource/cost constraints. No production connector is created without an existing integration contract.
