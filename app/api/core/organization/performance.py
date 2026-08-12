"""Synthetic performance and promotion evidence only."""
LEVELS = ("TRAINEE","JUNIOR","PROFESSIONAL","SENIOR","EXPERT","AUTONOMOUS","SUPERHUMAN","PERMANENT")
REQUIRED = ("sample_size", "task_definition", "metric", "confidence", "limitations")

def promotion_ready(evidence):
    return evidence.get("production_ready", False) and evidence.get("reliability", 0) >= 0.99 and evidence.get("accuracy", 0) >= 0.95 and evidence.get("human_review_rate", 1) <= 0.1
