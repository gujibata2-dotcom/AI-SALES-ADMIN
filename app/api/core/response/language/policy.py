SUPPORTED_LANGUAGES = frozenset({"th", "en", "zh", "ja", "ko"})

def select_language(customer_language: str, fallback: str = "en") -> str:
    value = customer_language.strip().lower()
    return value if value in SUPPORTED_LANGUAGES else fallback
