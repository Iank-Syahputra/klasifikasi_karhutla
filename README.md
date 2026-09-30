# Klasifikasi Karhutla — Deteksi Kebakaran Hutan & Lahan

Proyek Machine Learning untuk mengklasifikasikan potensi kebakaran hutan dan lahan
(Karhutla) berdasarkan data meteorologi harian, **lengkap dengan aplikasi website
Early Warning System (EWS)** yang menampilkan dashboard prediksi real-time.

> **Kenapa penting?** Karhutla berulang terjadi tiap musim kemarau dan berdampak
> langsung pada kesehatan, ekonomi, hingga iklim. Deteksi dini yang akurat dapat
> mempercepat respons dan meminimalkan kerugian.

---

## Ringkasan Hasil

| Metrik | Baseline (XGBoost) | Tuned | Tuned + Threshold 0.21 |
|--------|--------------------:|------:|--------------------------:|
| F1-Score (test 90:10) | **0.8667** | 0.8475 | **0.8652** |
| Accuracy | 0.8655 | 0.8487 | 0.8403 |
| ROC-AUC | 0.9219 | **0.9403** | 0.9403 |
| Gap accuracy (overfitting) | 3.16% | **2.22%** | – |
| CV F1 (5-fold) | 0.8359 | **0.8527** | – |
| Recall | 0.8387 | 0.8065 | **0.9839** |

- Model terbaik: **XGBoost tuned** dengan 4 fitur meteorologi dasar
  (`Temperature`, `Ws`, `Rain`, `RH`).
- Fitur FWI (FFMC, DMC, DC, ISI, BUI) **tidak digunakan** karena merupakan indeks bahaya
  yang sudah dirancang untuk prediksi (bersifat *circular reasoning*).
- Threshold optimal **0.21** menaikkan recall ke 98.4% — hampir semua kejadian kebakaran
  berhasil terdeteksi (penting untuk early warning).
- Semua hasil direproduksi deterministik (`random_state=42`).

---

## Struktur Repository

```
klasifikasi_karhutla/
├── notebooks/
│   └── karhutla.ipynb        # EDA → cleaning → modeling → tuning (hasil lengkap)
├── src/karhutla/             # Kode Python yang bisa di-import & diuji
│   ├── config.py             # Konfigurasi terpusat (path, fitur, threshold)
│   ├── data.py               # Pipeline pembersihan data
│   └── predict.py            # Memuat model & melakukan prediksi
├── api/                      # Backend FastAPI (Early Warning System)
│   ├── app/
│   │   ├── main.py           # Routes API + serve frontend di "/"
│   │   ├── schemas.py        # Validasi input/output (Pydantic)
│   │   ├── database.py       # Riwayat prediksi (SQLite)
│   │   └── service.py        # Gabungkan model ML + penyimpanan riwayat
│   └── ...
├── web/                      # Frontend dashboard EWS (HTML/CSS/JS + Chart.js)
│   ├── index.html
│   └── assets/
├── data/raw/                 # Dataset mentah (algerian_forest_fires.xlsx)
├── models/
│   └── xgboost_tuned.joblib  # Artefak model terbaik (siap dipakai, tanpa retrain)
├── docs/                     # Laporan, model card, temuan EDA
├── tests/                    # Unit test (pytest)
├── requirements.txt          # Dependencies (versi di-pin)
├── Makefile                  # Perintah umum
└── README.md
```

Ringkasan per folder:

| Folder | Isi | Untuk siapa |
|--------|-----|-------------|
| `notebooks/` | Eksplorasi & eksperimen lengkap | yang ingin memahami analisis |
| `src/karhutla/` | Kode produksi yang bisa di-import | yang ingin memakai/integrasi |
| `api/` | Backend FastAPI (predict, riwayat, stats) | aplikasi / deployment |
| `web/` | Dashboard EWS (form + grafik + riwayat) | pengguna website |
| `data/` | Bahan mentah dataset | reproduksibilitas |
| `models/` | Model terlatih (artefak) | aplikasi / deployment |
| `docs/` | Laporan & kartu model | stakeholder & reviewer |
| `tests/` | Pengaman kualitas kode | developer |

---

## Cara Menjalankan

### 1. Setup environment

```bash
# Buat virtual environment (disarankan)
python -m venv myvenv

# Aktifkan (Windows)
myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Lihat notebook (analisis lengkap)

```bash
jupyter notebook notebooks/karhutla.ipynb
```

Notebook sudah berisi **seluruh hasil output** (grafik & angka) sehingga bisa langsung
dibaca tanpa menjalankan ulang. Untuk memproduksi ulang semua hasil:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/karhutla.ipynb
```

> Notebook berjalan dari direktori mana pun berkat deteksi akar repositori otomatis.

### 3. Jalankan unit test

```bash
python -m pytest tests -v
```

### 4. Coba prediksi langsung

```python
from src.karhutla import predict_one

# Input: Temperature (°C), Ws (km/h), Rain (mm), RH (%)
hasil = predict_one({"Temperature": 34, "Ws": 20, "Rain": 0.0, "RH": 40})
print(hasil)
# {'fire': True, 'label': 'fire', 'probability': 0.8707, 'threshold': 0.21}
```

Artefak model disimpan di `models/xgboost_tuned.joblib` — dibuat oleh cell terakhir
("Export Model untuk Deployment") di notebook, sehingga prediksi **tanpa retrain**.

---

## Aplikasi Website — Early Warning System (EWS)

Website dashboard untuk mensimulasikan sistem peringatan dini: isi data cuaca,
dapatkan status risiko, dan pantau riwayat prediksi dalam grafik.

### Fitur

- **Form input cuaca** (Temperature, Ws, Rain, RH) dengan validasi.
- **Hasil prediksi real-time**: badge `fire`/`not fire`, probabilitas, dan threshold 0.21.
- **Riwayat prediksi** tersimpan (SQLite) + tabel riwayat.
- **Dashboard**: kartu ringkasan, grafik distribusi status, dan tren probabilitas.

### Menjalankan aplikasi

```bash
# dari akar repositori
uvicorn api.app.main:app --reload
```

Buka **http://localhost:8000** untuk dashboard. Dokumentasi API interaktif:
**http://localhost:8000/docs** (otomatis disediakan FastAPI).

### Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/health` | Status server |
| `POST` | `/api/v1/predict` | Prediksi kebakaran dari data cuaca (`{temperature, ws, rain, rh}`) |
| `GET` | `/api/v1/predictions?limit=50` | Riwayat prediksi terbaru |
| `GET` | `/api/v1/stats` | Ringkasan statistik riwayat |

Contoh request:

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 34, "ws": 20, "rain": 0.0, "rh": 40}'
```

```json
{"fire": true, "label": "fire", "probability": 0.8707, "threshold": 0.21}
```

--->

## Contoh Penggunaan `src`

```python
from src.karhutla import load_model, predict, predict_one

model_meta = load_model()                       # muat artefak model
hasil = predict([                               # prediksi beberapa baris
    {"Temperature": 40, "Ws": 15, "Rain": 0.0, "RH": 15},   # kondisi ekstrem panas-kering
    {"Temperature": 25, "Ws": 10, "Rain": 10.0, "RH": 90},  # kondisi sejuk-lembab
], model=model_meta)

print(hasil["labels"])         # ['fire', 'not fire']
print(hasil["probabilities"])  # [0.9431, 0.0066]
```

---

## Dataset

- **Sumber:** Extended Algerian Forest Fires Dataset (UCI Machine Learning Repository).
- **Isi:** 1.215 observasi harian kondisi cuaca dari **10 region** di Algeria
  (Juni–September 2021), 13 kolom.
- **Setelah cleaning:** 1.188 baris × 11 kolom; 27 baris duplikat silang-region dihapus
  (mencegah *data leakage*); tidak ada nilai hilang; kelas seimbang
  (fire 619 : not fire 569).

---

## Dokumentasi Lain

- [Laporan lengkap](docs/laporan.md) — narasi keseluruhan proyek.
- [Model Card](docs/model-card.md) — spesifikasi & limitasi model.
- [Temuan EDA](docs/temuan-eda.md) — ringkasan fakta dari explorasi data.

---

## Lisensi

Didistribusikan di bawah lisensi [MIT](LICENSE).