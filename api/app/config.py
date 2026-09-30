"""Konfigurasi aplikasi API Early Warning System.

Memanfaatkan konfigurasi paket ML (``src.karhutla.config``) agar path model
dan lokasi repositori konsisten. Path database dapat di-override lewat
variabel lingkungan ``KARHUTLA_DB_PATH`` (berguna untuk test/isolasi).
"""
import os

from src.karhutla.config import MODEL_PATH, THRESHOLD, get_repo_root

REPO_ROOT = get_repo_root()
WEB_DIR = REPO_ROOT / "web"

DEFAULT_DB_PATH = REPO_ROOT / "data" / "predictions.db"
DB_PATH = os.getenv("KARHUTLA_DB_PATH", str(DEFAULT_DB_PATH))

APP_NAME = "Karhutla Early Warning System"
APP_DESCRIPTION = (
    "API prediksi potensi kebakaran hutan dan lahan (Karhutla) "
    "berdasarkan data meteorologi harian."
)
APP_VERSION = "1.0.0"