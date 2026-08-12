def review_ip(prior_art_reviewed: bool, legal_review: bool = False) -> dict:
    if not prior_art_reviewed: return {"status":"IP_REVIEW_REQUIRED","patentability": "UNKNOWN"}
    return {"status":"IP_REVIEW_REQUIRED" if not legal_review else "LEGAL_REVIEW_COMPLETED","patentability":"UNKNOWN"}
