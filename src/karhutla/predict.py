"""Inferensi model — muat artefak dan lakukan prediksi.

Ini adalah modul yang akan dipanggil oleh aplikasi (misal API/website Early
Warning System) sehingga tidak perlu melatih ulang model setiap saat.
"""
from pathlib import Path

import joblib
import pandas as pd

from .config import CODE_TO_LABEL, FEATURES, MODEL_PATH


def load_model(path=None) -> dict:
    """Muat artefak model yang dihasilkan notebook (`models/xgboost_tuned.joblib`)."""
    path = Path(path) if path else MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Artefak model tidak ditemukan: {path}. "
            "Jalankan notebook (cell 'Export Model untuk Deployment') terlebih dahulu."
        )
    return joblib.load(path)


def _as_dataframe(X_new) -> pd.DataFrame:
    """Normalisasi input pengguna menjadi DataFrame dengan kolom fitur yang tepat."""
    if isinstance(X_new, dict):
        return pd.DataFrame([X_new])
    if isinstance(X_new, (list, tuple)):  # urutan mengikuti FEATURES
        return pd.DataFrame([dict(zip(FEATURES, X_new))])
    if isinstance(X_new, pd.DataFrame):
        return X_new.copy()
    raise ValueError("Input harus berupa dict, list/tuple, atau DataFrame")


def predict(X_new, model=None, threshold=None) -> dict:
    """Prediksi satu atau beberapa baris data meteorologi.

    Returns
    -------
    dict dengan kunci ``labels``, ``fire``, ``probabilities``, dan ``threshold``.
    """
    model = model if model is not None else load_model()
    threshold = (
        float(threshold)
        if threshold is not None
        else float(model["threshold"])
    )

    X = _as_dataframe(X_new)

    missing = [f for f in FEATURES if f not in X.columns]
    if missing:
        raise ValueError(f"Fitur yang dibutuhkan tidak ditemukan: {missing}")

    X = X[FEATURES]

    # Kolom probabilitas indeks 1 = kelas "fire"
    proba = model["model"].predict_proba(X)[:, 1]

    pred_code = (proba >= threshold).astype(int)
    pred_label = [CODE_TO_LABEL[code] for code in pred_code]

    return {
        "labels": pred_label,
        "fire": [label == "fire" for label in pred_label],
        "probabilities": proba.tolist(),
        "threshold": threshold,
    }


def predict_one(X_new, model=None, threshold=None) -> dict:
    """Prediksi satu baris input dan kembalikan hasil ringkas."""
    result = predict(X_new, model=model, threshold=threshold)
    return {
        "fire": result["fire"][0],
        "label": result["labels"][0],
        "probability": result["probabilities"][0],
        "threshold": result["threshold"],
    }