"""Phase 49 customer productization gateway."""
from .gateway import Customer199Gateway, ProductReadiness, ReadinessEvidence
from .payments import PaymentAdapter, PaymentEvent, StripePaymentAdapter
from .providers import ModelProvider, MockModelProvider, OpenAICompatibleProvider
from .trial import FreeTrialGateway, TrialReadiness, FREE_TRIAL_DAYS

__all__ = [
    "Customer199Gateway", "ProductReadiness", "ReadinessEvidence",
    "PaymentAdapter", "PaymentEvent", "StripePaymentAdapter",
    "ModelProvider", "MockModelProvider", "OpenAICompatibleProvider",
    "FreeTrialGateway", "TrialReadiness", "FREE_TRIAL_DAYS",
]
