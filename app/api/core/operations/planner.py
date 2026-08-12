from .models import ExecutionPlan

class PlanRejected(ValueError): pass

class PlanValidator:
    @staticmethod
    def validate(plan: ExecutionPlan) -> None:
        ids={t.task_id for t in plan.tasks}
        if len(ids)!=len(plan.tasks): raise PlanRejected("DUPLICATE_TASK_ID")
        if plan.max_parallel_tasks < 1 or plan.max_duration_seconds <= 0: raise PlanRejected("INVALID_EXECUTION_LIMIT")
        if plan.delegation_depth > plan.max_delegation_depth: raise PlanRejected("DELEGATION_DEPTH_EXCEEDED")
        graph={t.task_id:set(t.dependencies) for t in plan.tasks}
        for deps in graph.values():
            if not deps <= ids: raise PlanRejected("MISSING_DEPENDENCY")
        visiting=set(); visited=set()
        def visit(n):
            if n in visiting: raise PlanRejected("CIRCULAR_DEPENDENCY")
            if n in visited: return
            visiting.add(n)
            for d in graph[n]: visit(d)
            visiting.remove(n); visited.add(n)
        for n in graph: visit(n)
        for task in plan.tasks:
            for action in task.actions:
                if not action.authorization.approved: raise PlanRejected("UNAUTHORIZED_ACTION")
                if action.authorization.autonomy.value == "L5": raise PlanRejected("HUMAN_REQUIRED")
