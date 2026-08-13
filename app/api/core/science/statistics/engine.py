"""Scientific statistics helpers. Only report statistics that are actually computed."""
from math import sqrt

def descriptive(values: list[float]) -> dict:
    if not values: return {"status":"UNKNOWN"}
    n=len(values); mean=sum(values)/n; ordered=sorted(values); mid=n//2
    median=ordered[mid] if n%2 else (ordered[mid-1]+ordered[mid])/2
    variance=sum((x-mean)**2 for x in values)/(n-1) if n>1 else 0.0
    return {"sample_size":n,"mean":mean,"median":median,"variance":variance}

def correlation(x: list[float], y: list[float]) -> float | None:
    if len(x)!=len(y) or len(x)<2: return None
    mx=sum(x)/len(x); my=sum(y)/len(y)
    num=sum((a-mx)*(b-my) for a,b in zip(x,y)); dx=sum((a-mx)**2 for a in x); dy=sum((b-my)**2 for b in y)
    return num/sqrt(dx*dy) if dx and dy else None

def data_quality(values: list, expected_type: type | None = None) -> dict:
    missing=sum(v is None for v in values)
    invalid=sum(expected_type is not None and v is not None and not isinstance(v, expected_type) for v in values)
    return {"missing":missing,"invalid":invalid,"duplicate_count":len(values)-len({repr(v) for v in values})}
