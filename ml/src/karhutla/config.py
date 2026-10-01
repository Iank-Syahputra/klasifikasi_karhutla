"""Konfigurasi terpusat project Klasifikasi Karhutla.

Semua path, nama fitur, dan parameter (threshold) disimpan di satu tempat
agar mudah diubah tanpa menyentuh logika yang lain.
"""
from pathlib import Path

# Akar repositori = 3 tingkat di atas paket (ml/src/karhutla/config.py),
# dihitung relatif-paket sehingga kokoh dari direktori mana pun dijalankan.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ML_ROOT = PROJECT_ROOT / "ml"


DATA_PATH = ML_ROOT / "data" / "raw" / "algerian_forest_fires.xlsx"
MODEL_PATH = ML_ROOT / "models" / "xgboost_tuned.joblib"

# Fitur meteorologi dasar yang digunakan untuk prediksi
FEATURES = ["Temperature", "Ws", "Rain", "RH"]

TARGET_COL = "Classes"

# Threshold optimal hasil tuning (menghasilkan F1 tertinggi)
THRESHOLD = 0.21

# Hasil encoding target dari notebook
LABEL_TO_CODE = {"fire": 1, "not fire": 0}
CODE_TO_LABEL = {1: "fire", 0: "not fire"}