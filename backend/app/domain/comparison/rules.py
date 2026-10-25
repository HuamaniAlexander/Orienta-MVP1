from app.domain.errors import DomainError

CRITERIA = [
    ("description", "Enfoque de la carrera"),
    ("courses", "Cursos principales"),
    ("activities", "Actividades profesionales"),
    ("skills", "Habilidades a desarrollar"),
    ("field", "Campo laboral"),
    ("specialties", "Especialidades"),
    ("duration", "Duración"),
    ("practice", "Experiencia práctica"),
    ("qualification", "Grado y título"),
    ("cost", "Pensión mensual entre instituciones"),
    ("investment", "Inversión adicional"),
    ("environment", "Entornos de trabajo"),
]


def check_pair(ids):
    if len(ids) != 2 or ids[0] == ids[1]:
        raise DomainError("Selecciona dos carreras diferentes")


def comparison_rows(careers):
    return [
        {
            "key": key,
            "label": label,
            "values": [
                career["comparison"].get(key, "Ver planes institucionales") for career in careers
            ],
        }
        for key, label in CRITERIA
    ]
