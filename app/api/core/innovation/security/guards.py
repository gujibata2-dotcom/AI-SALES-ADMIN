def security_guard(code: str) -> dict:
    blocked = ("os.system", "subprocess", "eval(", "exec(", "rm -rf", "curl | sh", "wget | sh")
    hits = [x for x in blocked if x in code]
    return {"allowed": not hits, "findings": hits, "status": "BLOCKED" if hits else "REVIEW_REQUIRED"}
