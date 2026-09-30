"""Uji unit untuk API Early Warning System (FastAPI)."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.app import database as db  # noqa: E402
from api.app.main import app  # noqa: E402


@pytest.fixture()
def client(tmp_path):
    db.DB_PATH = str(tmp_path / "test_predictions.db")
    db.init_db()
    with TestClient(app) as c:
        yield c


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_root_serves_frontend(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_predict_valid(client):
    resp = client.post(
        "/api/v1/predict",
        json={"temperature": 40, "ws": 15, "rain": 0.0, "rh": 15},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["fire"] is True
    assert body["label"] == "fire"
    assert 0.0 <= body["probability"] <= 1.0
    assert body["threshold"] == pytest.approx(0.21, abs=1e-6)


def test_predict_safe_conditions(client):
    resp = client.post(
        "/api/v1/predict",
        json={"temperature": 25, "ws": 10, "rain": 10.0, "rh": 90},
    )
    assert resp.status_code == 200
    assert resp.json()["fire"] is False


def test_predict_validation_error(client):
    # rh = 150 di luar rentang valid (0-100)
    resp = client.post(
        "/api/v1/predict",
        json={"temperature": 40, "ws": 15, "rain": 0.0, "rh": 150},
    )
    assert resp.status_code == 422


def test_predict_missing_field(client):
    resp = client.post(
        "/api/v1/predict",
        json={"temperature": 40, "ws": 15, "rain": 0.0},
    )
    assert resp.status_code == 422


def test_predictions_recorded(client):
    client.post(
        "/api/v1/predict",
        json={"temperature": 40, "ws": 15, "rain": 0.0, "rh": 15},
    )
    resp = client.get("/api/v1/predictions")
    assert resp.status_code == 200
    rows = resp.json()
    assert len(rows) == 1
    assert rows[0]["label"] == "fire"
    assert rows[0]["rain"] == 0.0


def test_stats(client):
    client.post(
        "/api/v1/predict",
        json={"temperature": 40, "ws": 15, "rain": 0.0, "rh": 15},
    )
    client.post(
        "/api/v1/predict",
        json={"temperature": 25, "ws": 10, "rain": 10.0, "rh": 90},
    )
    resp = client.get("/api/v1/stats")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 2
    assert body["fire_count"] == 1
    assert body["not_fire_count"] == 1


def test_predictions_limit(client):
    for _ in range(5):
        client.post(
            "/api/v1/predict",
            json={"temperature": 40, "ws": 15, "rain": 0.0, "rh": 15},
        )
    resp = client.get("/api/v1/predictions", params={"limit": 3})
    assert len(resp.json()) == 3