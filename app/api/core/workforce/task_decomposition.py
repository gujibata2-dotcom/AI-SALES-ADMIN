"""Validate DAGs and build dependency-safe task plans."""
from collections import defaultdict, deque

def validate_dag(tasks: list[dict]) -> tuple[bool,str]:
    ids={t['task_id'] for t in tasks}
    indegree={i:0 for i in ids}; edges=defaultdict(list)
    for t in tasks:
        for dep in t.get('dependencies',[]):
            if dep not in ids: return False,f'UNKNOWN_DEPENDENCY:{dep}'
            edges[dep].append(t['task_id']); indegree[t['task_id']]+=1
    q=deque(i for i,d in indegree.items() if d==0); seen=0
    while q:
        n=q.popleft(); seen+=1
        for child in edges[n]:
            indegree[child]-=1
            if indegree[child]==0:q.append(child)
    return (seen==len(ids), 'CIRCULAR_DEPENDENCY' if seen!=len(ids) else 'VALID')

def ready_tasks(tasks:list[dict], completed:set[str]) -> list[dict]:
    return [t for t in tasks if t.get('status','PENDING')=='PENDING' and set(t.get('dependencies',[])).issubset(completed)]
