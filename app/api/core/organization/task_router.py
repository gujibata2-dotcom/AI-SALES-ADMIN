"""Deterministic task decomposition and dependency validation."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Task:
    task_id: str
    parent_task_id: str | None
    owner: str
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 0


def ready(task: Task, completed: set[str]) -> bool:
    return all(dep in completed for dep in task.dependencies)


def decompose(mission: str, objectives: list[str]) -> list[Task]:
    return [Task(f"task-{i+1}", None, "unassigned") for i, _ in enumerate(objectives)]
