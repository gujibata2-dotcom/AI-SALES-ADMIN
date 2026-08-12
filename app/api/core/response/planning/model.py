from dataclasses import dataclass

@dataclass(frozen=True)
class ResponsePlan:
    goal: str
    key_points: tuple[str, ...]
    required_sources: tuple[str, ...]
    language: str
    length: str = "short"
    tone: str = "natural"
    cta: str | None = None
    warnings: tuple[str, ...] = ()
    restrictions: tuple[str, ...] = ()
