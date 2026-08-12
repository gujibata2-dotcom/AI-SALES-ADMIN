from typing import Iterable, Dict, Any

def novelty_against_known(finding: str, known_findings: Iterable[str]) -> str:
    known = list(known_findings)
    if finding in known: return "KNOWN"
    if any(finding and (finding in x or x in finding) for x in known): return "PARTIALLY_NEW"
    return "UNCERTAIN"  # absence from the registry is not proof of discovery

def trend_signal(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = list(events)
    topics = [e.get("topic") for e in items if e.get("topic")]
    unique = set(topics)
    return {"status": "TREND" if len(topics) >= 3 and len(unique) < len(topics) else "SINGLE_EVENT", "observations": len(items)}
