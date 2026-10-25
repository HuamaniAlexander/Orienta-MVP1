"""Entrenamiento offline. No se generan etiquetas ni se promete exactitud."""

import argparse
import hashlib
import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from orienta_features.build import FEATURES
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def split_dataset(data):
    if data[FEATURES + ["participant_id", "y"]].isna().any().any():
        raise ValueError("Se requieren features completas, participante y etiqueta revisada")
    if set(data.y.unique()) != {0, 1}:
        raise ValueError("Se necesitan dos clases reales")
    if not data[FEATURES].apply(lambda col: col.between(0, 1).all()).all():
        raise ValueError("Features fuera del contrato")
    split = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    tr, te = next(split.split(data, data.y, data.participant_id))
    train, test = data.iloc[tr], data.iloc[te]
    if train.participant_id.nunique() < 5:
        raise ValueError("Se necesitan al menos cinco grupos de entrenamiento para este protocolo")
    folds = list(GroupKFold(5).split(train, train.y, train.participant_id))
    if set(test.y) != {0, 1} or any(
        set(train.iloc[a].y) != {0, 1} or set(train.iloc[b].y) != {0, 1} for a, b in folds
    ):
        raise ValueError("Las particiones no permiten evaluar ambas clases; reunir más datos")
    return train, test, folds


def train_model(csv_path, metadata_path, output):
    metadata = json.loads(Path(metadata_path).read_text())
    if (
        metadata.get("label_source") != "expert_review"
        or metadata.get("consent_documented") is not True
        or metadata.get("profiles_reviewed") is not True
    ):
        raise ValueError("El dataset requiere revisión experta y autorización documentadas")
    data = pd.read_csv(csv_path)
    train, test, folds = split_dataset(data)
    candidates = {
        "logistica": (LogisticRegression(max_iter=2000), {"model__C": [0.1, 1, 10]}),
        "arbol": (
            DecisionTreeClassifier(random_state=42),
            {"model__max_depth": [2, 4], "model__min_samples_leaf": [5, 10]},
        ),
        "bosque": (
            RandomForestClassifier(n_estimators=200, random_state=42),
            {"model__max_depth": [3, 6], "model__min_samples_leaf": [5, 10]},
        ),
        "dummy": (DummyClassifier(strategy="most_frequent"), {}),
    }
    searches = {}
    for name, (model, grid) in candidates.items():
        search = GridSearchCV(
            Pipeline([("scale", StandardScaler()), ("model", model)]),
            grid,
            cv=folds,
            scoring="f1_macro",
            error_score="raise",
        )
        search.fit(train[FEATURES], train.y)
        searches[name] = search
    selected = max(searches, key=lambda name: searches[name].best_score_)
    # La elección queda congelada ANTES de abrir las predicciones del test.
    reports = {}
    for name, search in searches.items():
        pred = search.predict(test[FEATURES])
        reports[name] = {
            "cv_f1_macro": float(search.best_score_),
            "accuracy": float(accuracy_score(test.y, pred)),
            "report": classification_report(
                test.y, pred, labels=[0, 1], output_dict=True, zero_division=0
            ),
            "confusion_matrix": confusion_matrix(test.y, pred, labels=[0, 1]).tolist(),
        }
    # Referencia por contenido: umbral elegido exclusivamente en train/CV.
    from sklearn.metrics import f1_score

    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
    scores = {
        threshold: sum(
            f1_score(
                train.iloc[b].y,
                (train.iloc[b][FEATURES].mean(axis=1) >= threshold).astype(int),
                average="macro",
                zero_division=0,
            )
            for _, b in folds
        )
        / len(folds)
        for threshold in thresholds
    }
    threshold = max(scores, key=scores.get)
    pred_baseline = (test[FEATURES].mean(axis=1) >= threshold).astype(int)
    reports["contenido"] = {
        "threshold": threshold,
        "accuracy": float(accuracy_score(test.y, pred_baseline)),
        "report": classification_report(test.y, pred_baseline, output_dict=True, zero_division=0),
    }
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    artifact = output / "pipeline.joblib"
    joblib.dump(searches[selected].best_estimator_, artifact)
    manifest = {
        "version": "experimento-1",
        "status": "experimental",
        "features": FEATURES,
        "selected_by_cv": selected,
        "sklearn_version": sklearn.__version__,
        "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
        "dataset_sha256": hashlib.sha256(Path(csv_path).read_bytes()).hexdigest(),
        "questionnaire_version": "q1",
        "metadata": metadata,
        "train_participants": int(train.participant_id.nunique()),
        "test_participants": int(test.participant_id.nunique()),
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (output / "metrics.json").write_text(json.dumps(reports, indent=2))
    (output / "model_card.md").write_text(
        "# Modelo experimental\n\nPredice una etiqueta experta de afinidad, no éxito vocacional.\nRequiere revisión de errores, incertidumbre y criterios de promoción antes de aprobar.\n"
    )
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--output", type=Path, default=Path("ml/artifacts/experiment"))
    args = parser.parse_args()
    result = train_model(args.csv, args.metadata, args.output)
    print(json.dumps({"status": result["status"], "selected_by_cv": result["selected_by_cv"]}))
