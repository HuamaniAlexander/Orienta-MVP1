from decimal import Decimal


def feasibility(offer, conditions):
    result = {}
    modalities = conditions.get("modalities", [])
    result["modality"] = (
        ("compatible" if offer["modality"] in modalities else "incompatible")
        if modalities
        else "no_preference"
    )
    districts = conditions.get("districts", [])
    result["district"] = (
        ("compatible" if offer.get("district") in districts else "incompatible")
        if districts and offer.get("district")
        else "no_preference"
        if not districts
        else "review_institution"
    )
    budget = conditions.get("monthly_budget")
    if budget is None:
        result["budget"] = "no_preference"
    elif offer["cost_status"] != "verificado" or offer["cost"] is None:
        result["budget"] = "review_source"
    else:
        result["budget"] = (
            "compatible" if Decimal(offer["cost"]) <= Decimal(str(budget)) else "incompatible"
        )
    max_months = conditions.get("max_months")
    result["duration"] = (
        ("compatible" if offer["months"] <= max_months else "incompatible")
        if max_months
        else "no_preference"
    )
    formation = conditions.get("formation", "cualquiera")
    result["formation"] = (
        "no_preference"
        if formation == "cualquiera"
        else ("compatible" if offer.get("formation") == formation else "incompatible")
    )
    return result
