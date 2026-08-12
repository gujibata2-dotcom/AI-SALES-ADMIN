# Execution Safety

Every workflow declares allowed_actions, allowed_targets, allowed_data, allowed_channels, max_duration, retry/backoff/timeout limits, parallelism and budget. Scope cannot be widened by an Agent or delegated child. Financial, legal, security and irreversible actions are human-gated.

Success is reported only after expected-vs-actual verification. Transport success is not business success.
