def maturity(status: str) -> dict:
    order={"IDEA":0,"CONCEPT":1,"DESIGN":2,"PROTOTYPE":3,"EXPERIMENTAL":4,"VALIDATED":5,"PRODUCTION_READY":6,"DEPLOYED":7}
    return {"status":status,"level":order.get(status, -1)}
