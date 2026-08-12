"""Evidence-based role matching; recommendations never grant permissions."""

DIMENSIONS = ("capability_fit", "reliability_fit", "experience_fit", "risk_fit", "cost_fit", "availability_fit")


def match_role(profile: dict, role: dict) -> dict:
    required = set(role.get("required_capabilities", []))
    actual = set(profile.get("capabilities", []))
    capability_fit = len(required & actual) / len(required) if required else 0.0
    return {"role_id": role.get("role_id"), "capability_fit": capability_fit,
            "reliability_fit": profile.get("reliability_fit", 0),
            "experience_fit": profile.get("experience_fit", 0),
            "risk_fit": profile.get("risk_fit", 0), "cost_fit": profile.get("cost_fit", 0),
            "availability_fit": profile.get("availability_fit", 0), "status": "RECOMMEND" if capability_fit else "NO_MATCH"}
