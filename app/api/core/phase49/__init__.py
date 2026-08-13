"""Phase 49 customer productization gateway.

This package closes the 199-Baht execution path around existing Phase 44/45
runtime primitives. It deliberately keeps payment and model providers behind
small adapters so tests never fake a live payment or AI provider.
"""
from .gateway import Customer199Gateway, ProductReadiness, ReadinessEvidence
from .payments import PaymentAdapter, PaymentEvent, StripePaymentAdapter
from .providers import ModelProvider, MockModelProvider, OpenAICompatibleProvider

__all__ = [
    "Customer199Gateway", "ProductReadiness", "ReadinessEvidence",
    "PaymentAdapter", "PaymentEvent", "StripePaymentAdapter",
    "ModelProvider", "MockModelProvider", "OpenAICompatibleProvider",
]
