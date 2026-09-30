"""Entry point aplikasi FastAPI Early Warning System.

Menjalankan:
    uvicorn api.app.main:app --reload

Frontend (``web/``) disajikan langsung oleh FastAPI di ``/``.
Dokumentasi API interaktif tersedia di ``/docs``.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import APP_DESCRIPTION, APP_NAME, APP_VERSION, WEB_DIR
from . import database as db
from . import schemas
from . import service


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.get("/health", tags=["sistem"])
def health():
    return {"status": "ok", "message": "Karhutla EWS siap."}


@app.post(
    "/api/v1/predict",
    response_model=schemas.PredictionOutput,
    tags=["prediksi"],
    summary="Prediksi potensi kebakaran dari data cuaca",
)
def predict(payload: schemas.PredictionInput):
    return service.predict_and_record(payload)


@app.get(
    "/api/v1/predictions",
    response_model=list[schemas.PredictionRecord],
    tags=["riwayat"],
    summary="Ambil riwayat prediksi terbaru",
)
def predictions(limit: int = 50):
    return db.list_predictions(limit)


@app.get(
    "/api/v1/stats",
    response_model=schemas.Stats,
    tags=["riwayat"],
    summary="Ringkasan statistik riwayat prediksi",
)
def stats():
    return db.get_stats()


# Frontend disajikan terakhir agar route API lebih dulu dicocokkan.
app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")