"""Klasifikasi Karhutla — paket Python untuk prediksi kebakaran hutan dan lahan.

Modul utama:
- ``data.py``    : pembersihan & penyiapan data
- ``predict.py`` : muat model & inferensi (dipakai integrasi aplikasi nanti)
- ``config.py``  : konfigurasi terpusat
"""
from .config import FEATURES, THRESHOLD
from .data import clean_data, load_clean_data, load_raw_data, prepare_features
from .predict import load_model, predict, predict_one

__version__ = "1.0.0"

__all__ = [
    "clean_data",
    "load_clean_data",
    "load_raw_data",
    "prepare_features",
    "load_model",
    "predict",
    "predict_one",
    "FEATURES",
    "THRESHOLD",
]