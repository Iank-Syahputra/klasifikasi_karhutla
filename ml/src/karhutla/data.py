"""Pembersihan dan penyiapan data — replikasi bagian Data Cleaning dari notebook."""
from pathlib import Path

import pandas as pd

from .config import DATA_PATH, FEATURES, LABEL_TO_CODE, TARGET_COL


def load_raw_data(path=None) -> pd.DataFrame:
    """Muat dataset mentah dari file Excel."""
    path = Path(path) if path else DATA_PATH
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan di: {path}")
    return pd.read_excel(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan dataset mentah sesuai alur notebook.

    Langkah:
    1. Bersihkan nama kolom (whitespace & karakter kutip tunggal).
    2. Normalisasi nilai kolom target (``Classes``).
    3. Drop kolom identitas (``DATE`` dan ``Bejaia 2021``).
    4. Hapus baris duplikat silang-region berdasarkan fitur.
    """
    df = df.copy()

    # 1. Bersihkan nama kolom
    df.columns = df.columns.str.strip().str.strip("'").str.strip()

    # 2. Normalisasi nilai kelas
    df[TARGET_COL] = df[TARGET_COL].str.strip()

    # 3. Drop kolom identitas yang tidak relevan untuk prediksi
    df.drop(columns=["DATE", "Bejaia 2021"], inplace=True)

    # 4. Hapus duplikat (fitur identik antar region) untuk mencegah data leakage
    feature_cols = [c for c in df.columns if c != TARGET_COL]
    df = df.drop_duplicates(subset=feature_cols, keep="first").reset_index(drop=True)

    return df


def prepare_features(df: pd.DataFrame):
    """Pisahkan X (fitur meteorologi) dan y (target ter-encode 0/1)."""
    X = df[FEATURES].copy()
    y = df[TARGET_COL].map(LABEL_TO_CODE)
    return X, y


def load_clean_data(path=None):
    """Jalankan seluruh pipeline data: muat -> bersihkan -> siapkan fitur."""
    df = load_raw_data(path)
    df = clean_data(df)
    return prepare_features(df)