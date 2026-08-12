from dataclasses import dataclass
from .models import ActionRequest, RiskLevel, AutonomyLevel

@dataclass(frozen=True)
class GatewayDecision:
    allowed: bool
    reason: str

class ActionGateway:
    """Default-deny policy choke point. External adapters are intentionally absent."""
    def __init__(self, budget: float=0.0, rate_limit: int=10):
        self.budget=budget; self.rate_limit=rate_limit; self.spent=0.0; self.calls=0; self.stopped=False; self.keys=set()

    def authorize(self, action: ActionRequest) -> GatewayDecision:
        a=action.authorization
        if self.stopped: return GatewayDecision(False, "KILL_SWITCH_ACTIVE")
        if a.autonomy in {AutonomyLevel.L0, AutonomyLevel.L5} or a.human_required: return GatewayDecision(False, "HUMAN_REQUIRED")
        if not a.approved: return GatewayDecision(False, "AUTHORIZATION_REQUIRED")
        if action.allowed_actions and action.action_type not in action.allowed_actions: return GatewayDecision(False, "ACTION_OUT_OF_SCOPE")
        if action.allowed_targets and action.target not in action.allowed_targets: return GatewayDecision(False, "TARGET_OUT_OF_SCOPE")
        if action.risk_level is RiskLevel.CRITICAL: return GatewayDecision(False, "CRITICAL_ACTION_HUMAN_GATE")
        if action.cost < 0 or self.spent + action.cost > self.budget: return GatewayDecision(False, "BUDGET_EXCEEDED")
        if self.calls >= self.rate_limit: return GatewayDecision(False, "RATE_LIMIT_EXCEEDED")
        if action.idempotency_key and action.idempotency_key in self.keys: return GatewayDecision(False, "DUPLICATE_EXECUTION")
        if action.timeout_seconds <= 0 or action.max_retries < 0: return GatewayDecision(False, "INVALID_LIMIT")
        return GatewayDecision(True, "AUTHORIZED")

    def record(self, action: ActionRequest) -> None:
        self.spent += action.cost; self.calls += 1
        if action.idempotency_key: self.keys.add(action.idempotency_key)

    def stop(self) -> None: self.stopped=True
    def resume(self) -> None: self.stopped=False
