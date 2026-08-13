# Adaptive Strategy

Strategy versions are immutable historical records. Adaptation requires a trigger and evidence references. Supported triggers include new evidence, forecast failure, market/technology/risk/objective/capability/regulatory change.

Strategy drift reports observed changes; a numeric drift score is `UNKNOWN` unless a documented measurement basis exists.

Loop: Strategy → Decision → Authorized Handoff → Outcome → Environment → New Intelligence → Re-evaluate → Strategy Version.
