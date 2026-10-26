"""Inferencia TF-IDF pura sobre artefacto JSON entrenado fuera de las solicitudes."""

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

ANCHORS = {
    "Q01": (
        "lógica y análisis",
        "logica analisis razonamiento datos problemas estadistica matematicas",
    ),
    "Q02": (
        "investigación científica",
        "ciencias investigacion cientifica evidencia salud enfermedad biologia",
    ),
    "Q03": (
        "tecnología",
        "tecnologia programacion software sistemas datos aplicaciones seguridad informatica",
    ),
    "Q04": (
        "cuidado de personas",
        "personas pacientes cuidado salud atencion bienestar prevencion comunidad",
    ),
    "Q05": (
        "gestión",
        "gestion empresas recursos finanzas operaciones organizacion planificacion negocios",
    ),
    "Q06": (
        "creación y comunicación",
        "creatividad comunicacion diseno espacios representacion argumentacion proyectos",
    ),
    "Q07": (
        "análisis e investigación",
        "analisis investigacion datos metodos cientificos procesos estadistica",
    ),
    "Q08": ("colaboración", "equipos personas comunicacion gestion colaboracion organizaciones"),
}


class ContentEngine:
    def __init__(self, artifact):
        path = Path(artifact)
        raw = path.read_bytes()
        model = json.loads(raw)
        manifest = json.loads(path.with_suffix(".manifest.json").read_text())
        if hashlib.sha256(raw).hexdigest() != manifest["artifact_sha256"]:
            raise ValueError("El artefacto de contenido no coincide con su manifest")
        if model["format"] != "orienta-tfidf-1" or len(model["idf"]) != len(model["vocabulary"]):
            raise ValueError("Formato de contenido incompatible")
        self.vocabulary = {word: i for i, word in enumerate(model["vocabulary"])}
        self.terms = model["vocabulary"]
        self.idf = model["idf"]
        self.stop = set(model["stop_words"])
        self.documents = {d["career_id"]: d for d in model["documents"]}
        self.version = model["version"]
        self.anchors = {qid: self.transform(text) for qid, (_, text) in ANCHORS.items()}

    def transform(self, text):
        text = "".join(
            c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c)
        )
        words = [w for w in re.findall(r"(?u)\b\w\w+\b", text) if w not in self.stop]
        counts = Counter(words + [" ".join(pair) for pair in zip(words, words[1:])])
        vector = {
            self.vocabulary[w]: (1 + math.log(n)) * self.idf[self.vocabulary[w]]
            for w, n in counts.items()
            if w in self.vocabulary
        }
        norm = math.sqrt(sum(v * v for v in vector.values()))
        return {i: v / norm for i, v in vector.items()} if norm else {}

    def evaluate(self, responses, career_id):
        document = self.documents.get(career_id)
        known = [qid for qid in ANCHORS if responses.get(qid) is not None]
        if len(known) < 4 or not document:
            return {
                "score": None,
                "coverage": len(known),
                "reasons": [],
                "status": "insufficient_information",
            }
        if any(type(responses[qid]) is not int or not 1 <= responses[qid] <= 5 for qid in known):
            raise ValueError("Respuestas fuera del contrato del cuestionario")
        query = {}
        for qid in known:
            weight = (responses[qid] - 1) / 4
            for index, value in self.anchors[qid].items():
                query[index] = query.get(index, 0) + weight * value
        norm = math.sqrt(sum(v * v for v in query.values()))
        if not norm:
            return {"score": None, "coverage": len(known), "reasons": [], "status": "explore_more"}
        query = {i: v / norm for i, v in query.items()}
        vector = {int(i): v for i, v in document["vector"].items()}
        score = sum(v * vector.get(i, 0) for i, v in query.items())
        reasons = []
        for qid in known:
            if responses[qid] < 3:
                continue
            overlaps = {
                i: value * vector.get(i, 0)
                for i, value in self.anchors[qid].items()
                if vector.get(i, 0) > 0
            }
            if not overlaps:
                continue
            terms = [self.terms[i] for i in sorted(overlaps, key=overlaps.get, reverse=True)[:3]]
            reasons.append(
                {
                    "id": f"{career_id}:contenido:{qid}",
                    "dimension": qid,
                    "text": f"Tu interés por {ANCHORS[qid][0]} coincide con temas del programa: {', '.join(terms)}.",
                    "weight": sum(overlaps.values()) * (responses[qid] - 1) / 4,
                }
            )
        reasons.sort(key=lambda item: item["weight"], reverse=True)
        return {
            "score": round(max(0, min(1, score)) * 100, 2),
            "coverage": len(known),
            "status": "available",
            "reasons": [
                {k: v for k, v in reason.items() if k != "weight"} for reason in reasons[:3]
            ],
            "source_url": document["source_url"],
            "model_version": self.version,
        }
