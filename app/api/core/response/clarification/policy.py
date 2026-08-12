def should_clarify(*, intent_clear: bool, product_clear: bool, requirements_complete: bool, source_conflict: bool, critical_missing: bool) -> bool:
    return not intent_clear or not product_clear or not requirements_complete or source_conflict or critical_missing
