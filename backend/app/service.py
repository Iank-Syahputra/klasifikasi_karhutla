"""Lapisan bisnis: menggabungkan model ML dan penyimpanan riwayat."""
from ml.src.karhutla import load_model, predict_one

from . import database as db
from .schemas import PredictionInput, PredictionOutput


def predict_and_record(payload: PredictionInput) -> PredictionOutput:
    """Jalankan prediksi dari input API lalu simpan ke riwayat database."""
    model = load_model()

    result = predict_one(
        {
            "Temperature": payload.temperature,
            "Ws": payload.ws,
            "Rain": payload.rain,
            "RH": payload.rh,
        },
        model=model,
    )

    db.insert_prediction(
        temperature=payload.temperature,
        ws=payload.ws,
        rain=payload.rain,
        rh=payload.rh,
        probability=result["probability"],
        fire=result["fire"],
        label=result["label"],
    )

    return PredictionOutput(
        fire=result["fire"],
        label=result["label"],
        probability=result["probability"],
        threshold=result["threshold"],
    )