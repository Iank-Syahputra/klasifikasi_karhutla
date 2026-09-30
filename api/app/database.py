"""Akses database SQLite (stdlib) untuk riwayat prediksi.

Tidak memerlukan dependency tambahan. ``DB_PATH`` dapat di-override
(utama untuk keperluan test agar tidak mengotori database lokal).
"""
import sqlite3
from pathlib import Path

from .config import DB_PATH

DB_PATH = str(DB_PATH)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    ws          REAL NOT NULL,
    rain        REAL NOT NULL,
    rh          REAL NOT NULL,
    probability REAL NOT NULL,
    fire        INTEGER NOT NULL,
    label       TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def _connect():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Pastikan tabel riwayat prediksi ada."""
    with _connect() as conn:
        conn.execute(_SCHEMA)


def insert_prediction(
    temperature: float,
    ws: float,
    rain: float,
    rh: float,
    probability: float,
    fire: bool,
    label: str,
) -> int:
    """Simpan satu riwayat prediksi, kembalikan id baris baru."""
    with _connect() as conn:
        conn.execute(_SCHEMA)
        cur = conn.execute(
            """
            INSERT INTO predictions
                (temperature, ws, rain, rh, probability, fire, label)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (temperature, ws, rain, rh, probability, int(fire), label),
        )
        return cur.lastrowid


def list_predictions(limit: int = 50) -> list[dict]:
    """Ambil riwayat prediksi terbaru (default 50 baris)."""
    limit = max(1, min(int(limit), 500))
    with _connect() as conn:
        conn.execute(_SCHEMA)
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


def get_stats() -> dict:
    """Ringkasan statistik seluruh riwayat prediksi."""
    with _connect() as conn:
        conn.execute(_SCHEMA)
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        fire_count = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE label = 'fire'"
        ).fetchone()[0]
        not_fire_count = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE label = 'not fire'"
        ).fetchone()[0]
        avg = conn.execute(
            "SELECT AVG(probability) FROM predictions"
        ).fetchone()[0]
    return {
        "total": int(total),
        "fire_count": int(fire_count),
        "not_fire_count": int(not_fire_count),
        "avg_probability": round(float(avg or 0.0), 4),
    }