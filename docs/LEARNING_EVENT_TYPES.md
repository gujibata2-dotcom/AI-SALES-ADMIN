# Event Types

| Event | Meaning |
|---|---|
| RESPONSE_SUCCESS | Response passed operational validation/outcome criteria |
| RESPONSE_FAILURE | Response failed one or more criteria |
| CUSTOMER_CLARIFICATION | Customer had to clarify the request |
| CUSTOMER_CORRECTION | Customer corrected a detail |
| HUMAN_CORRECTION | Human corrected an AI output |
| KNOWLEDGE_MISS | Required knowledge was not available to the response path |
| KNOWLEDGE_CONFLICT | Candidate sources disagree |
| RETRIEVAL_FAILURE | Retrieval failed to surface usable existing knowledge |
| LOW_CONFIDENCE | Confidence threshold was not met |
| WORKFLOW_FAILURE | Workflow could not complete as designed |
| ACTION_FAILURE | An external/internal action failed |
| ESCALATION | Case was escalated |
| CUSTOMER_REJECTION | Customer rejected a recommendation/offer/response |
| CUSTOMER_ACCEPTANCE | Customer accepted a response/recommendation/outcome; never equates automatically to product quality |
| CUSTOMER_FEEDBACK | Explicit customer feedback |

Correlation is not causation. Repeated acceptance, conversion, or rejection is evidence for analysis, not proof of why an outcome occurred.
