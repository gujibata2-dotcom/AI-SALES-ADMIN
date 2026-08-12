"""Evidence-weighted consensus; never majority-only."""

def consensus(proposals):
    if not proposals: raise ValueError("No proposals")
    ranked = sorted(proposals, key=lambda p: (p.get("evidence_quality",0), p.get("confidence",0), p.get("specialization",0)), reverse=True)
    top = ranked[0]
    if len(ranked) > 1 and top.get("evidence_quality",0) == ranked[1].get("evidence_quality",0) and top.get("confidence",0) == ranked[1].get("confidence",0):
        return {"status":"REVIEW", "reason":"unresolved evidence tie"}
    return {"status":"RESOLVED", "decision":top.get("decision"), "evidence":top.get("evidence", [])}
