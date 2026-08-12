def compare_designs(designs: list[dict]) -> dict:
    fields = ("cost","performance","complexity","risk","maintainability","scalability")
    return {"designs": [{k: d.get(k, "UNKNOWN") for k in fields} for d in designs], "winner": "UNDETERMINED"}
