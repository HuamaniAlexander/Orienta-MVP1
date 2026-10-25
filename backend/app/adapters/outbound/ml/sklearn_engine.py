import hashlib
import json
from pathlib import Path

from orienta_features.build import FEATURES, complete_features


class SklearnSignal:
    def __init__(self, directory):
        path = Path(directory)
        manifest = json.loads((path / "manifest.json").read_text())
        artifact = path / "pipeline.joblib"
        if manifest.get("status") != "approved" or manifest.get("features") != FEATURES:
            raise ValueError("Modelo no aprobado o contrato incompatible")
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != manifest.get("sha256"):
            raise ValueError("Hash de modelo inválido")
        import joblib
        import sklearn
        if manifest.get("sklearn_version") != sklearn.__version__:
            raise ValueError("Versión scikit-learn incompatible")
        self.pipeline = joblib.load(artifact)  # Solo artefactos propios aprobados.
        self.version = manifest["version"]

    def predict(self, responses, profile):
        import pandas as pd
        frame = pd.DataFrame([complete_features(responses, profile)], columns=FEATURES)
        index = list(self.pipeline.classes_).index(1)
        return float(self.pipeline.predict_proba(frame)[0, index])
