# Phase 48 Business Intelligence

Phase 48 separates observed business facts from inference, prediction, simulation and recommendation. Business events and metrics retain source/provenance and timestamps. Business state is `UNKNOWN` when evidence is insufficient.

Decision recommendations never equal decisions. High/critical decisions require authorization and execution is delegated to Phase 47 through its workflow gate.

Forecasts return `FORECAST_UNAVAILABLE` below the configured data-quality threshold. Simulation outputs are explicitly labeled `SIMULATION`; inferred relationships are not presented as causal facts.
