"""Uji unit untuk pipeline data (replikasi Data Cleaning di notebook)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.karhutla.config import DATA_PATH
from src.karhutla.data import clean_data, load_clean_data, load_raw_data


def test_dataset_exists():
    assert DATA_PATH.exists()


def test_load_raw_data_shape():
    df = load_raw_data()
    assert df.shape == (1215, 13)


def test_clean_data_removes_duplicates():
    df = clean_data(load_raw_data())
    # 1215 - 27 duplikat silang-region = 1188
    assert df.shape[0] == 1188
    assert df.shape[1] == 11  # drop DATE & Bejaia 2021


def test_clean_data_classes_normalized():
    df = clean_data(load_raw_data())
    assert set(df["Classes"].unique()) == {"fire", "not fire"}


def test_clean_data_no_missing():
    df = clean_data(load_raw_data())
    assert df.isnull().sum().sum() == 0


def test_load_clean_data_returns_consistent_features():
    X, y = load_clean_data()
    assert list(X.columns) == ["Temperature", "Ws", "Rain", "RH"]
    assert set(y.unique()) == {0, 1}
    assert len(X) == len(y) == 1188