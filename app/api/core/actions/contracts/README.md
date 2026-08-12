# Action Contracts

## Action Request
`action_id`, `task_id`, `action_type`, `target_type`, `target_reference`, `parameters_reference`, `requested_by`, `authorization`, `risk_level`, `knowledge_sources`, `timestamp`.

## Action Result
`action_id`, `status`, `result_reference`, `verification`, `warnings`, `error`, `timestamp`.

References are opaque. Never place secrets, credentials, passwords, payment data, or unnecessary PII in contracts.