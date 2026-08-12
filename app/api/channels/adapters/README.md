# Channel Adapter Contract

Adapters expose receive(), normalize(), send(), verify(), health(). Phase 15 uses mock/sandbox. Production integrations must execute through Phase 14 Action Gateway; no direct LLM → channel send path.