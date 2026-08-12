from .models import ExecutionPlan, ExecutionResult, ExecutionStatus, VerificationStatus
from .planner import PlanValidator
from .gateway import ActionGateway

class ExecutionEngine:
    def __init__(self, gateway: ActionGateway): self.gateway=gateway

    def run(self, execution_id: str, plan: ExecutionPlan) -> ExecutionResult:
        PlanValidator.validate(plan)
        completed=set(); retries=0
        for task in plan.tasks:
            if not set(task.dependencies) <= completed:
                return ExecutionResult(execution_id, ExecutionStatus.FAILED, VerificationStatus.FAILED, error="DEPENDENCY_NOT_COMPLETE")
            for action in task.actions:
                decision=self.gateway.authorize(action)
                if not decision.allowed:
                    return ExecutionResult(execution_id, ExecutionStatus.ESCALATED, VerificationStatus.UNKNOWN, error=decision.reason)
                self.gateway.record(action)
            completed.add(task.task_id)
        return ExecutionResult(execution_id, ExecutionStatus.COMPLETED, VerificationStatus.SUCCESS, result={"tasks_completed":len(completed),"retries":retries})

    @staticmethod
    def classify_verification(expected, actual):
        if actual is None: return VerificationStatus.UNKNOWN
        if expected == actual: return VerificationStatus.SUCCESS
        if isinstance(expected, dict) and isinstance(actual, dict) and expected.keys() & actual.keys(): return VerificationStatus.PARTIAL_SUCCESS
        return VerificationStatus.FAILED
