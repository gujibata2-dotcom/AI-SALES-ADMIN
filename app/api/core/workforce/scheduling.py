"""Workload-aware scheduling abstraction."""
def priority_score(t:dict)->float:
    return (2*t.get('business_value',0)+2*t.get('risk',0)+t.get('urgency',0)+t.get('deadline_pressure',0)+t.get('dependency_count',0))

def schedule(tasks:list[dict])->list[dict]:
    return sorted(tasks,key=priority_score,reverse=True)

def overloaded(workload:float,capacity:float)->bool:
    return workload>capacity
