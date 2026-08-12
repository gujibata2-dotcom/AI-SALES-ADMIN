"""Explainable career recommendations; recommendations never approve themselves."""


def next_recommendations(profile: dict) -> dict:
    gaps = profile.get("skill_gaps", [])
    return {"best_next_role": profile.get("role_recommendation"),
            "best_next_skill": gaps[0].get("skill") if gaps else None,
            "best_training": gaps[0].get("training") if gaps else None,
            "best_benchmark": profile.get("next_benchmark"),
            "promotion_readiness": profile.get("promotion_readiness", "NOT_EVALUATED"),
            "specialization_opportunity": profile.get("specialization_opportunity", "NOT_EVALUATED")}
