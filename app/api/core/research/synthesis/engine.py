from ..models import Claim, Evidence
from .engine import synthesize

def run(claims: list[Claim], evidence: list[Evidence]) -> dict:
    return synthesize(claims, evidence)
