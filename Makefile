.PHONY: setup notebook train test app predict

## Setup environment: install semua dependencies
setup:
	pip install -r requirements.txt

## Buka notebook untuk eksplorasi & analisis
notebook:
	jupyter notebook ml/notebooks/karhutla.ipynb

## Jalankan ulang seluruh notebook (menghasilkan ulang artefak model di ml/models/)
train:
	jupyter nbconvert --to notebook --execute --inplace ml/notebooks/karhutla.ipynb

## Jalankan unit test (ML + backend API)
test:
	python -m pytest ml/tests backend/tests -v

## Jalankan aplikasi website Early Warning System (buka http://localhost:8000)
app:
	uvicorn backend.app.main:app --reload

## Contoh prediksi cepat
predict:
	python -c "from ml.src.karhutla import predict_one; print(predict_one({'Temperature': 34, 'Ws': 20, 'Rain': 0.0, 'RH': 40}))"