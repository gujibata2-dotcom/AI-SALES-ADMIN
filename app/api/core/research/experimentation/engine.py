from ..engine import ResearchEngine
from ..models import Experiment

def authorize(experiment: Experiment, risk: str) -> dict:
    return ResearchEngine().authorize_experiment(risk, experiment.authorization)
