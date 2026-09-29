"""Konfigurasi terpusat project Klasifikasi Karhutla.

Semua path, nama fitur, dan parameter (threshold) disimpan di satu tempat
agar mudah diubah tanpa menyentuh logika yang lain.
"""
from pathlib import Path


def get_repo_root() -> Path:
    """Deteksi akar repositori (folder yang berisi folder ``data/``).

    Bekerja dari direktori mana pun di dalam tree repositori.
    """
    root = Path.cwd()
    while not (root / "data").is_dir():
        root = root.parent
    return root


DATA_PATH = get_repo_root() / "data" / "raw" / "algerian_forest_fires.xlsx"
MODEL_PATH = get_repo_root() / "models" / "xgboost_tuned.joblib"

# Fitur meteorologi dasar yang digunakan untuk prediksi
FEATURES = ["Temperature", "Ws", "Rain", "RH"]

TARGET_COL = "Classes"

# Threshold optimal hasil tuning (menghasilkan F1 tertinggi)
THRESHOLD = 0.21

# Hasil encoding target dari notebook
LABEL_TO_CODE = {"fire": 1, "not fire": 0}
CODE_TO_LABEL = {1: "fire", 0: "not fire"}