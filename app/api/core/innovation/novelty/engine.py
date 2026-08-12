def check_novelty(knowledge_checked: bool, product_checked: bool, methods_checked: bool, patents_checked: bool) -> str:
    if not all((knowledge_checked, product_checked, methods_checked, patents_checked)): return "UNKNOWN"
    return "POTENTIALLY_NEW"
