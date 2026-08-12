# Integration Adapter Architecture

```text
AI Core
  ↓
Action Layer
  ↓
Integration Interface
  ↓
Adapter
  ↓
External Service (future only)
```

Core code must not know provider-specific API details. Phase 10 contains mock adapters only.