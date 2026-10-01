"""Konfigurasi aplikasi API Early Warning System.

Memanfaatkan konfigurasi paket ML (``ml.src.karhutla.config``) agar path model
dan lokasi repositori konsisten. Path database dapat di-override lewat
variabel lingkungan ``KARHUTLA_DB_PATH`` (berguna untuk test/isolasi).
"""
import os
from pathlib import Path

from ml.src.karhutla.config import MODEL_PATH, THRESHOLD

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = PROJECT_ROOT / "frontend"

DEFAULT_DB_PATH = PROJECT_ROOT / "backend" / "data" / "predictions.db"
DB_PATH = os.getenv("KARHUTLA_DB_PATH", str(DEFAULT_DB_PATH))

APP_NAME = "Karhutla Early Warning System"
APP_DESCRIPTION = (
    "API prediksi potensi kebakaran hutan dan lahan (Karhutla) "
    "berdasarkan data meteorologi harian."
)
APP_VERSION = "1.0.0"