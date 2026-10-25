import pandas as pd
import pytest
from orienta_features.build import FEATURES, build_profile, complete_features

from ml.src.train import split_dataset


def test_shared_features_and_missing_values():
    data = {f"Q{i:02}": 5 for i in range(1, 9)}
    assert list(complete_features(data, [1] * 6)) == FEATURES
    assert list(complete_features(data, [1] * 6).values()) == [1] * 6
    data["Q03"] = None
    assert build_profile(data)[2] is None
    with pytest.raises(ValueError, match="seis dimensiones"):
        complete_features(data, [1] * 6)


def test_group_split_has_no_participant_leakage():
    # Dataset sintético EXCLUSIVAMENTE para probar separación, no métricas reales.
    rows = [
        {"participant_id": p, "y": y, **dict.fromkeys(FEATURES, 0.6)}
        for p in range(30)
        for y in [0, 1]
    ]
    train, test, folds = split_dataset(pd.DataFrame(rows))
    assert set(train.participant_id).isdisjoint(test.participant_id)
    for a, b in folds:
        assert set(train.iloc[a].participant_id).isdisjoint(train.iloc[b].participant_id)


def test_one_class_is_rejected():
    data = pd.DataFrame([{"participant_id": 1, "y": 1, **dict.fromkeys(FEATURES, 0.5)}])
    with pytest.raises(ValueError, match="dos clases"):
        split_dataset(data)
