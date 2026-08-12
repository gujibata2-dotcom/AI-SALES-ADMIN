from dataclasses import dataclass

@dataclass(frozen=True)
class Draft:
    draft_text: str
    language: str
    sources: tuple[str, ...]
    claims: tuple[str, ...]
    warnings: tuple[str, ...]
    confidence: float
