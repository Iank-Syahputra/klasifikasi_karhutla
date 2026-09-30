"""Uji unit untuk modul prediksi (inferensi model)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.karhutla.config import MODEL_PATH
from src.karhutla.predict import load_model, predict, predict_one


def test_model_artifact_exists():
    assert MODEL_PATH.exists(), "Jalankan notebook terlebih dahulu untuk menghasilkan artefak model"


def test_load_model():
    meta = load_model()
    assert "model" in meta
    assert meta["features"] == ["Temperature", "Ws", "Rain", "RH"]
    assert abs(meta["threshold"] - 0.21) < 1e-6
    assert "best_params" in meta
    assert "metrics_split" in meta


def test_predict_dict_input():
    result = predict_one({"Temperature": 33, "Ws": 20, "Rain": 0.0, "RH": 55})
    assert 0.0 <= result["probability"] <= 1.0
    assert result["fire"] in (True, False)
    assert result["label"] in ("fire", "not fire")
    assert abs(result["threshold"] - 0.21) < 1e-6


def test_predict_list_input():
    # urutan input mengikuti FEATURES: [Temperature, Ws, Rain, RH]
    result = predict_one([40, 15, 0.0, 15])
    assert result["fire"] is True
    assert result["label"] == "fire"


def test_predict_single_rows():
    result = predict({"Temperature": 40, "Ws": 15, "Rain": 0.0, "RH": 15})
    assert result["fire"] == [True]
    assert result["labels"] == ["fire"]


def test_extreme_fire_conditions_high_probability():
    result = predict_one({"Temperature": 40, "Ws": 15, "Rain": 0.0, "RH": 15})
    assert result["probability"] > 0.5


def test_extreme_safe_conditions_low_probability():
    result = predict_one({"Temperature": 25, "Ws": 10, "Rain": 10.0, "RH": 90})
    assert result["probability"] < 0.5


def test_custom_threshold_parameter():
    # threshold sangat rendah -> semua baris diklasifikasikan fire
    result = predict_one(
        {"Temperature": 25, "Ws": 10, "Rain": 10.0, "RH": 90}, threshold=0.001
    )
    assert result["fire"] is True


def test_missing_feature_raises_error():
    with pytest.raises(ValueError):
        predict_one({"Temperature": 33, "Ws": 20})