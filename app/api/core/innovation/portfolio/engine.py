def portfolio(items: list[dict]) -> dict:
    counts={k:0 for k in ("IDEA","CONCEPT","PROTOTYPE","EXPERIMENTAL","VALIDATED","DEPLOYED")}
    for item in items:
        if item.get("status") in counts: counts[item["status"]]+=1
    return {"counts":counts,"conversion_rate":None,"activity_is_success":False}
