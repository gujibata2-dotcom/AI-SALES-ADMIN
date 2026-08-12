def novelty_against_known(finding: str, known_findings: list[str]) -> str:
    if finding in known_findings:
        return "KNOWN"
    if any(finding and (finding in item or item in finding) for item in known_findings):
        return "PARTIALLY_NEW"
    return "UNCERTAIN"
