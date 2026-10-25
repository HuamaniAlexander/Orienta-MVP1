DIMENSIONS = ("logica", "ciencia", "tecnologia", "personas", "gestion", "comunicacion")
FEATURES = ["sim_" + key for key in DIMENSIONS]
MAPPING = (("Q01", "Q07"), ("Q02", "Q07"), ("Q03",), ("Q04", "Q08"), ("Q05", "Q08"), ("Q06", "Q08"))


def build_profile(responses):
    values = []
    for questions in MAPPING:
        known = [responses[q] for q in questions if responses.get(q) is not None]
        if any(type(v) is not int or not 1 <= v <= 5 for v in known):
            raise ValueError("Las respuestas deben ser enteros 1–5 o null")
        values.append((sum(known) / len(known) - 1) / 4 if known else None)
    return values


def similarities(responses, career_profile):
    if len(career_profile) != 6 or any(not 0 <= x <= 1 for x in career_profile):
        raise ValueError("Perfil académico inválido")
    return [
        1 - abs(u - c) if u is not None else None
        for u, c in zip(build_profile(responses), career_profile)
    ]


def complete_features(responses, career_profile):
    values = similarities(responses, career_profile)
    if any(v is None for v in values):
        raise ValueError("El modelo supervisado exige las seis dimensiones conocidas")
    return dict(zip(FEATURES, values))
