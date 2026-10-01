# Model Card — XGBoost Klasifikasi Karhutla

> Kartu model ringkas untuk memudahkan siapa pun (termasuk non-ahli) memahami
> model ini: data yang dipakai, cara kerjanya, seberapa bagus, dan keterbatasannya.

---

## 1. Ringkasan

- **Tugas:** Klasifikasi biner — prediksi potensi **kebakaran hutan/lahan** (fire) vs tanpa kebakaran (not fire).
- **Model:** XGBoost Classifier (tuned via RandomizedSearchCV).
- **Input:** 4 variabel meteorologi harian.
- **Output:** Probabilitas kebakaran + label `fire` / `not fire` (menggunakan threshold 0.21).

## 2. Dataset

- **Sumber:** Extended Algerian Forest Fires Dataset (UCI ML Repository), 10 region di Algeria, Juni–September 2021.
- **Ukuran awal:** 1.215 baris × 13 kolom.
- **Setelah cleaning:** 1.188 baris × 11 kolom.
  - 27 baris duplikat silang-region dihapus (mencegah data leakage).
  - Drop kolom identitas `DATE` dan `Bejaia 2021`.
  - Tidak ada nilai hilang.
- **Distribusi kelas:** fire 619 (52.1%) : not fire 569 (47.9%) — seimbang.

## 3. Fitur

| Fitur | Deskripsi |
|-------|-----------|
| `Temperature` | Suhu udara (°C) |
| `Ws` | Kecepatan angin (km/h) |
| `Rain` | Curah hujan (mm) |
| `RH` | Kelembaban relatif (%) |

**Fitur FWI (FFMC, DMC, DC, ISI, BUI, FWI) sengaja TIDAK dipakai** karena merupakan
indeks bahaya kebakaran (bersifat *circular reasoning*).

**Feature importance (model tuned):**

| Fitur | Importance |
|-------|-----------:|
| Rain | 0.5363 |
| RH | 0.2359 |
| Temperature | 0.1740 |
| Ws | 0.0538 |

## 4. Performa

Hasil deterministik (`random_state=42`) pada split 90:10 dan cross-validation:

| Metrik | Tuned (test) | Tuned (5-fold CV) |
|--------|-------------:|------------------:|
| Accuracy | 0.8487 | 0.8476 ± 0.0259 |
| Precision | 0.8929 | 0.8581 ± 0.0246 |
| Recall | 0.8065 | 0.8482 ± 0.0378 |
| F1-Score | 0.8475 | 0.8527 ± 0.0260 |
| ROC-AUC | 0.9403 | 0.9166 ± 0.0248 |

**Threshold tuning:** pada threshold 0.21, F1 naik ke **0.8652** dengan recall **0.9839**
(hampir semua kebakaran terdeteksi — vital untuk early warning).

## 5. Keputusan Desain

- **Hyperparameter terbaik:** `subsample=0.7`, `reg_lambda=1`, `reg_alpha=1`,
  `n_estimators=150`, `min_child_weight=9`, `max_depth=5`, `learning_rate=0.05`,
  `gamma=0.2`, `colsample_bytree=0.7`; best CV F1 = **0.8576**.
- **Overfitting:** gap accuracy 2.22% (Good Fit) — tuning memperkecil gap dari baseline (3.16%).
- **Tree-based model** dipilih karena tahan terhadap multikolinearitas & outlier,
  dan tidak menuntut normalitas data.

## 6. Limitasi & Catatan Penggunaan

1. **Data geografis terbatas** — dilatih pada data Algeria; sifat kebakaran di
   Indonesia (gambut, lahan rawa) dapat berbeda. Untuk produksi EWS di Indonesia,
   perlu validasi dengan data lokal.
2. **Input terbatas 4 fitur cuaca** — tidak mencakup faktor manusia (pembakaran lahan,
   hot spot), tutupan lahan, maupun angin berlebih.
3. **Prediksi harian** = indikator risiko, **bukan** kepastian kejadian; keputusan
   operasional tetap memerlukan konfirmasi lapangan.
4. Model menggunakan **threshold 0.21** secara default — aplikasi dapat menyesuaikan
   untuk mengubah trade-off false positive / false negative.
5. Artefak model bersifat **versi data**; jika dataset diperbarui, ulangi pelatihan.

## 7. Cara Pakai

```python
from src.karhutla import predict_one
predict_one({"Temperature": 34, "Ws": 20, "Rain": 0.0, "RH": 40})
```

## 8. Reproduksibilitas

- Semua langkah dijelaskan selangkah demi selangkah di `ml/notebooks/karhutla.ipynb`.
- `requirements.txt` mem-pin seluruh versi dependency.
- Dataset mentah tersedia di `ml/data/raw/`.