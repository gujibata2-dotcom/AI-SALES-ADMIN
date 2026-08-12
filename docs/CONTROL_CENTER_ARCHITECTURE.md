# Control Center Architecture

```mermaid
flowchart TD
  A[AI Employee] --> B[Core Engines]
  B --> C[Control Center API]
  C --> D[Control Center Web]
  D --> E[Human Administrator]
  B --> C
  C --> F[Audit]
```

The Control Center is the control plane, not the AI brain. It observes Conversation, Knowledge, Decision, Orchestration, Action, Learning, Customer, Sales, and Support state. Critical mutations require authorized human control.
