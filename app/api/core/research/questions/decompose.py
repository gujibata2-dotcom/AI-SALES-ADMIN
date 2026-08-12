def decompose(question: str, dependencies: dict[str, list[str]] | None = None) -> dict:
    return {"question": question, "sub_questions": list((dependencies or {}).keys()), "dependencies": dependencies or {}}
