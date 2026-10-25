from orienta_features.build import DIMENSIONS, similarities


def affinity(responses, profile):
    values = similarities(responses, profile)
    known = [v for v in values if v is not None]
    contributions = [{"dimension": key, "similarity": round(v, 4)}
                     for key, v in zip(DIMENSIONS, values) if v is not None]
    return {"index": round(100 * sum(known) / len(known), 2) if len(known) >= 4 else None,
            "coverage": len(known), "dimensions": 6, "contributions": contributions}


def preference(results):
    scores = [r["affinity"]["index"] for r in results]
    if any(s is None for s in scores):
        return {"status": "insufficient_evidence", "career_id": None}
    if max(scores) < 50:
        return {"status": "explore_more", "career_id": None}
    if abs(scores[0] - scores[1]) < 5:
        return {"status": "similar_affinity", "career_id": None}
    return {"status": "higher_affinity", "career_id": results[scores.index(max(scores))]["career_id"]}
