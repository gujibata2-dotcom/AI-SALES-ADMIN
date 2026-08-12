"""Portfolio model keeps output separate from outcome."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PortfolioItem:
    portfolio_id: str
    project_id: str
    strategic_alignment: list[str]
    expected_outcome: str
    cost: float | None
    risk: str
    status: str = "NOT_EVALUATED"
