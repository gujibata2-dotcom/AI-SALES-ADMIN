# Change requests

Fields: `change_id`, `type`, `reason`, `source`, `risk`, `impact`, `proposed_change`, `evaluation_reference`, `approval`, `status`.

Lifecycle: DRAFT → EVALUATING → REVIEW_REQUIRED → APPROVED → VERSIONED → CANARY → DEPLOYED, or REJECTED.

Allowed change types: prompt, policy, knowledge, workflow, agent configuration, evaluation criteria, and content rules.

No change may bypass policy, authorization, Action Gateway, safety gates, or human approval requirements.