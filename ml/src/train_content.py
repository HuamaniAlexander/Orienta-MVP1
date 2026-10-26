"""Entrena TF-IDF sobre contenido académico real; exporta JSON sin pickle ni etiquetas ficticias."""

import argparse
import hashlib
import json
from pathlib import Path

STOP_WORDS = "a al algo algunas algunos ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha hacia hasta hay la las le les lo los mas me mi muy no nos o otra otras otro otros para pero por porque que quien se ser si sin sobre son su sus te tiene todo todos tu tus un una unas uno unos y ya".split()


def train(corpus_path, output):
    import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer

    raw = Path(corpus_path).read_bytes()
    records = json.loads(raw)
    ids = [r["career_id"] for r in records]
    if len(ids) != len(set(ids)) or len(ids) < 2:
        raise ValueError("Se necesitan documentos únicos de al menos dos carreras")
    if any(not r["text"].strip() or not r["source_url"].startswith("https://") for r in records):
        raise ValueError("Cada documento necesita texto y fuente HTTPS")
    vectorizer = TfidfVectorizer(
        strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True, stop_words=STOP_WORDS
    )
    matrix = vectorizer.fit_transform(r["text"] for r in records)
    model = {
        "format": "orienta-tfidf-1",
        "method": "content_based",
        "version": "contenido-" + hashlib.sha256(raw).hexdigest()[:12],
        "corpus_sha256": hashlib.sha256(raw).hexdigest(),
        "sklearn_version": sklearn.__version__,
        "stop_words": STOP_WORDS,
        "vocabulary": vectorizer.get_feature_names_out().tolist(),
        "idf": vectorizer.idf_.tolist(),
        "documents": [
            dict(
                career_id=r["career_id"],
                source_url=r["source_url"],
                text_sha256=hashlib.sha256(r["text"].encode()).hexdigest(),
                vector={str(i): float(matrix[n, i]) for i in matrix[n].indices},
            )
            for n, r in enumerate(records)
        ],
    }
    dest = Path(output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(model, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    manifest = {
        "method": "TF-IDF + similitud coseno",
        "documents": len(records),
        "features": matrix.shape[1],
        "corpus_sha256": model["corpus_sha256"],
        "artifact_sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
        "supervised": False,
        "interpretation": "Coincidencia temática, no probabilidad de éxito ni aptitud validada",
    }
    dest.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", default="data/ml/corpus_carreras.json")
    parser.add_argument("--output", default="data/models/contenido.json")
    args = parser.parse_args()
    print(json.dumps(train(args.corpus, args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
