.PHONY: setup notebook train test predict

## Setup environment: install semua dependencies
setup:
	pip install -r requirements.txt

## Buka notebook untuk eksplorasi & analisis
notebook:
	jupyter notebook notebooks/karhutla.ipynb

## Jalankan ulang seluruh notebook (menghasilkan ulang artefak model di models/)
train:
	jupyter nbconvert --to notebook --execute --inplace notebooks/karhutla.ipynb

## Jalankan unit test
test:
	python -m pytest tests -v

## Contoh prediksi cepat
predict:
	python -c "from src.karhutla import predict_one; print(predict_one({'Temperature': 34, 'Ws': 20, 'Rain': 0.0, 'RH': 40}))"