"""Kontrak data (Pydantic) untuk request dan response API."""
from typing import Literal

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    """Input prediksi: 4 variabel meteorologi harian."""

    temperature: float = Field(..., ge=-20, le=60, description="Suhu udara (Celsius)")
    ws: float = Field(..., ge=0, le=200, description="Kecepatan angin (km/jam)")
    rain: float = Field(..., ge=0, le=300, description="Curah hujan (mm)")
    rh: float = Field(..., ge=0, le=100, description="Kelembaban relatif (%)")


class PredictionOutput(BaseModel):
    """Hasil prediksi satu baris data."""

    fire: bool
    label: Literal["fire", "not fire"]
    probability: float = Field(..., ge=0, le=1)
    threshold: float = Field(..., ge=0, le=1)


class PredictionRecord(BaseModel):
    """Satu baris riwayat prediksi yang tersimpan di database."""

    id: int
    temperature: float
    ws: float
    rain: float
    rh: float
    probability: float
    fire: bool
    label: str
    created_at: str


class Stats(BaseModel):
    """Ringkasan statistik riwayat prediksi untuk dashboard."""

    total: int
    fire_count: int
    not_fire_count: int
    avg_probability: float