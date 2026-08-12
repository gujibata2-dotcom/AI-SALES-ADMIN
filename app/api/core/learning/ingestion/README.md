# Learning Events

Learning ingestion accepts outcome and feedback references from operational systems. Use reference IDs rather than raw customer data.

Allowed event types: RESPONSE_SUCCESS, RESPONSE_FAILURE, CUSTOMER_CLARIFICATION, CUSTOMER_CORRECTION, HUMAN_CORRECTION, KNOWLEDGE_MISS, KNOWLEDGE_CONFLICT, RETRIEVAL_FAILURE, LOW_CONFIDENCE, WORKFLOW_FAILURE, ACTION_FAILURE, ESCALATION, CUSTOMER_REJECTION, CUSTOMER_ACCEPTANCE, CUSTOMER_FEEDBACK.

Permitted inputs include conversation/task/sales outcomes, human corrections, clarification and objection signals, retrieval/validation/workflow/action results, escalation results, customer feedback, and approved recommendation history.

Never ingest passwords, API keys, payment credentials, unnecessary PII, or sensitive profiling data. Privacy classification is mandatory.

A human correction is evidence, not automatically a new source of truth. It must be verified against authoritative knowledge before becoming publishable knowledge.
