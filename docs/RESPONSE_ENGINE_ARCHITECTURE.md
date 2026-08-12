# Response Engine Architecture

```mermaid
flowchart TD
  A[Conversation Understanding] --> D[Response Decision]
  B[Knowledge Retrieval] --> D
  C[Ethics] --> D
  E[Sales Rules] --> D
  F[Personality] --> D
  D --> G[Response Planning]
  G --> H[Generation]
  H --> I[Validation]
  I --> J[Final Response Candidate]
  J --> K[Human Escalation / Delivery Layer]
```

Delivery Layer is not implemented in Phase 8.
