# Model

## `xgboost_tuned.joblib`

Artefak model terbaik yang dihasilkan oleh `ml/notebooks/karhutla.ipynb`
(cell **"Export Model untuk Deployment"**).

Isi file (dict yang di-*dump* dengan `joblib`):

| Key | Keterangan |
|-----|------------|
| `model` | Objek `XGBClassifier` tuned (sudah di-`fit`) |
| `features` | `["Temperature", "Ws", "Rain", "RH"]` |
| `threshold` | 0.21 (threshold optimal hasil tuning) |
| `best_params` | Hyperparameter terbaik dari RandomizedSearchCV |
| `cv_f1_best` | Best CV F1 = 0.8576 |
| `metrics_split` | Metrik pada split terbaik (test F1 0.8475, AUC 0.9403) |
| `n_samples` / `n_features` | Ukuran data pelatihan |

Cara memuat dan memakai:

```python
from ml.src.karhutla import load_model, predict_one

meta = load_model()                      # default: ml/models/xgboost_tuned.joblib
hasil = predict_one({"Temperature": 34, "Ws": 20, "Rain": 0.0, "RH": 40}, model=meta)
```

Cara membuat ulang artefak ini (langkah resmi, bukan di-download):

```bash
jupyter nbconvert --to notebook --execute --inplace ml/notebooks/karhutla.ipynb
```

Model dilatih pada data kehutanan Algeria (4 fitur meteorologi dasar). Detail &
limitasi: lihat [docs/model-card.md](../docs/model-card.md).