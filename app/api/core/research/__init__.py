"""Phase 36 AI Research & Discovery Engine.

Evidence-first, auditable research primitives with no external side effects.
"""
from .models import ResearchQuestion, ResearchProject, Source, Evidence, Claim, Hypothesis, Experiment, ResearchFinding, ResearchReview, KnowledgeGap
from .engine import ResearchEngine

__all__ = ["ResearchEngine", "ResearchQuestion", "ResearchProject", "Source", "Evidence", "Claim", "Hypothesis", "Experiment", "ResearchFinding", "ResearchReview", "KnowledgeGap"]
