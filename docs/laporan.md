# Laporan Klasifikasi Karhutla

Proyek ini membangun model Machine Learning untuk mendeteksi potensi **kebakaran
hutan dan lahan (Karhutla)** dari data meteorologi harian, sebagai fondasi untuk
sistem peringatan dini (Early Warning System) berbasis website.

---

## 1. Latar Belakang & Masalah

Kebakaran hutan dan lahan terjadi berulang setiap musim kemarau dan berdampak luas:
kesehatan masyarakat, aktivitas ekonomi, hingga iklim regional. Pemantauan konvensional
(pengawasan langsung, citra satelit) lambat dan tidak menjangkau semua area.

**Pertanyaan yang dijawab proyek ini:** dapatkah kondisi cuaca harian memprediksi
potensi kebakaran secara otomatis dan akurat?

## 2. Data

- **Sumber:** Extended Algerian Forest Fires Dataset (UCI ML Repository).
- **Isi:** 1.215 observasi harian dari **10 region** di Algeria (Juni–September 2021),
  13 kolom. Setiap baris = kondisi cuaca + status kebakaran (`fire`/`not fire`).
- **Kolom:** `DATE`, `Temperature`, `Ws`, `Rain`, `RH`, indeks FWI
  (`FFMC`, `DMC`, `DC`, `ISI`, `BUI`, `FWI`), `Classes`, `Bejaia 2021`.

## 3. Eksplorasi Data (EDA)

- **Kelas seimbang** (fire 52.1% : not fire 47.9%) → tidak perlu resampling.
- **Pola kuat:** kebakaran terkonsentrasi saat `FFMC > 80`; hujan >0 hampir selalu
  `not fire`; kebakaran dominan saat suhu 35–38°C dan RH rendah.
- **Multikolinearitas tinggi** antar indeks FWI (DMC–BUI r = 0.98) → tree-based model
  tidak terpengaruh; indeks FWI tidak dipakai karena *circular reasoning*.
  Detail lengkap: [temuan-eda.md](temuan-eda.md).

## 4. Pembersihan Data

1. Bersihkan nama kolom (whitespace & kutip tunggal).
2. Normalisasi nilai kelas `Classes`.
3. Drop kolom identitas `DATE` dan `Bejaia 2021`.
4. **Deduplikasi:** 27 baris duplikat silang-region dihapus (mencegah data leakage).

Hasil akhir: **1.188 × 11**, tanpa nilai hilang.

## 5. Pemodelan

- **Fitur:** 4 fitur meteorologi dasar (`Temperature`, `Ws`, `Rain`, `RH`).
- **Algoritma:** Decision Tree, Random Forest, XGBoost — seluruhnya dengan regularisasi.
- **Evaluasi:** 3 variasi split (70:30, 80:20, 90:10) + 5-fold cross-validation.

Hasil baseline (test set):

| Model | Split 70:30 F1 | Split 80:20 F1 | Split 90:10 F1 |
|-------|--------------:|--------------:|--------------:|
| Decision Tree | 0.8451 | 0.8139 | 0.8235 |
| Random Forest | 0.8564 | 0.8512 | 0.8644 |
| XGBoost | **0.8610** | 0.8430 | **0.8667** |

- **XGBoost 90:10 terbaik** (Test F1 0.8667, Acc 0.8655, AUC 0.9219, Good Fit).
- Satu-satunya *Mild Overfitting*: XGBoost 80:20 (gap 5.76%).

## 6. Hyperparameter Tuning

RandomizedSearchCV (100 iterasi, 5-fold, scoring F1) menghasilkan **best CV F1 0.8576**
dengan kombinasi regularisasi kuat (`subsample=0.7`, `max_depth=5`, `gamma=0.2`, …).

Hasil tuned pada split 90:10:

- AUC naik **0.9219 → 0.9403**.
- Gap accuracy turun **3.16% → 2.22%** (lebih generalisasi).
- F1 test sedikit turun (0.8667 → 0.8475) karena perubahan distribusi probabilitas.

## 7. Threshold Tuning

Distribusi probabilitas berubah, sehingga threshold default 0.5 tidak optimal.
Threshold optimal **0.21**:

- F1 naik ke **0.8652**.
- Recall naik ke **0.9839** — hampir semua kebakaran terdeteksi (sangat penting untuk
  early warning, meski menambah false positive).

## 8. Kesimpulan

1. **XGBoost tuned + threshold 0.21** menjadi model rekomendasi (F1 0.8652, recall 0.9839,
   AUC 0.9403).
2. Cukup **4 variabel cuaca** untuk prediksi yang baik — indeks FWI tidak diperlukan.
3. Pipeline bersih, deterministik, dan **reproducible** (README, unit test, versi di-pin).

## 9. Rekomendasi Selanjutnya

- **Integrasi API/website:** serving model via `src/karhutla/predict.py` untuk
  membangun antarmuka Early Warning System.
- **Validasi data lokal Indonesia** (karakteristik gambut/tanah berbeda).
- **Eksperimen fitur tambahan** (misal indeks kekeringan lokal, data lahan).