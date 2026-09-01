# Proyek Pengembangan dan Pengoperasian Sistem Machine Learning

**Username Dicoding:** `reza_harahap`  
**Dataset:** Breast Cancer Wisconsin (Diagnostic)  
**Masalah:** klasifikasi biner tumor ganas/jinak berdasarkan 30 fitur numerik hasil pemeriksaan sel.  

## Solusi
Pipeline TFX memakai Apache Beam dengan komponen ExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, **Tuner**, Trainer, Resolver, Evaluator, dan Pusher. Model utama adalah neural network binary classifier. Evaluasi menggunakan Binary Accuracy dan AUC dengan threshold kelulusan 0.90.

## Baseline lokal yang tervalidasi di paket ini
Baseline scikit-learn Logistic Regression (bukan pengganti TFX) dipakai hanya untuk smoke-test dataset di environment pembuatan paket. Hasil: **AUC 0.9954**, **Binary Accuracy 0.9825**.

## Deployment
`Dockerfile` menggunakan TensorFlow Serving. Jalankan pipeline lebih dulu agar `serving_model/` berisi SavedModel yang dipush oleh TFX, lalu build/deploy image ke Railway/Heroku atau platform container cloud.

## Monitoring
Folder `monitoring/` berisi Prometheus dan provisioning Grafana. `docker-compose.yml` disediakan untuk menjalankan model serving, Prometheus, dan Grafana secara lokal.

## Web App / Model Serving URL
`<ISI_URL_CLOUD_SETELAH_DEPLOYMENT_NYATA>`

## Hasil Monitoring
`<ISI_RINGKASAN_SETELAH_PROMETHEUS_GRAFANA_BERJALAN_DI_CLOUD>`

## Cara Menjalankan
1. Gunakan Python 3.10 dan virtualenv baru.
2. `pip install -r requirements.txt`
3. `python pipeline.py`
4. Pastikan SavedModel tersedia pada `serving_model/`.
5. `docker compose up --build`
6. Jalankan `reza_harahap-testing.ipynb` untuk request prediksi.

## Catatan integritas bukti
Berkas di `evidence/` menjelaskan screenshot yang wajib diambil dari deployment/monitoring nyata. Paket ini **tidak memalsukan screenshot cloud**.
