def preserve_context(passage: str, context: str) -> dict:
    return {"passage": passage, "context": context, "context_preserved": bool(context.strip())}
