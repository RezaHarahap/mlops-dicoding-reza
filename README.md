# Submission 1: Breast Cancer Classification MLOps

**Nama:** Muhammad Reza Pahlevi Harahap  
**Username Dicoding:** `reza_harahap`

| | Deskripsi |
| ----------- | ----------- |
| Dataset | **Breast Cancer Wisconsin (Diagnostic)**. Dataset submission berada pada `data/breast_cancer.csv` dan terdiri dari **569 observasi**, **30 fitur numerik**, serta satu label biner. Distribusi label pada berkas yang dipakai pipeline adalah 212 sampel label 0 dan 357 sampel label 1. |
| Masalah | Proyek menyelesaikan klasifikasi biner karakteristik tumor payudara berdasarkan fitur numerik hasil pengukuran inti sel. Sistem tidak hanya melatih model, tetapi juga membangun pipeline data/model yang reproducible, menyiapkan model untuk serving, melakukan deployment, serta memonitor layanan produksi. |
| Solusi machine learning | Solusi dibangun sebagai **TensorFlow Extended (TFX) pipeline** menggunakan `BeamDagRunner`. Komponen yang digunakan adalah `CsvExampleGen`, `StatisticsGen`, `SchemaGen`, `ExampleValidator`, `Transform`, `Tuner`, `Trainer`, `Resolver`, `Evaluator`, dan `Pusher`. Model yang lolos evaluasi dipush ke `serving_model/` sebagai TensorFlow SavedModel. |
| Metode pengolahan | `CsvExampleGen` membagi input menjadi contoh train/eval dan menyimpannya sebagai TFRecord. `StatisticsGen` menghasilkan statistik fitur, `SchemaGen` membuat schema, dan `ExampleValidator` memeriksa anomali. Pada `Transform`, seluruh 30 fitur numerik distandardisasi menggunakan z-score (`tft.scale_to_z_score`), sedangkan label dipertahankan sebagai integer untuk klasifikasi biner. |
| Arsitektur model | Model dibuat dengan Keras Functional API. Tiga hyperparameter dicari oleh `Tuner`: learning rate, jumlah hidden units, dan dropout. Arsitektur Trainer terdiri dari input untuk seluruh fitur transformed, concatenation, Dense ReLU, Dropout, Dense ReLU kedua, dan output Dense 1 neuron dengan aktivasi sigmoid. Optimizer yang digunakan adalah Adam dan loss `binary_crossentropy`. |
| Metrik evaluasi | Metrik pelatihan dan evaluasi adalah **Binary Accuracy** dan **AUC**. `Evaluator` menggunakan TensorFlow Model Analysis dengan model-spec signature `serving_default`. Pipeline menetapkan acceptance threshold minimal **0.90** untuk Binary Accuracy dan **0.90** untuk AUC sebelum model dapat diberkati dan dipush. |
| Performa model | Performa model divalidasi oleh komponen `Evaluator`; model hanya diteruskan ke `Pusher` apabila memenuhi threshold Binary Accuracy ≥ 0.90 dan AUC ≥ 0.90. Artifact evaluasi nyata disertakan pada direktori `reza_harahap-pipeline/Evaluator/`, sedangkan SavedModel hasil model yang diberkati disertakan pada `serving_model/`. |
| Opsi deployment | Model dipaketkan menggunakan **TensorFlow Serving 2.15.1** di dalam Docker container dan dideploy ke **Railway**. REST API TensorFlow Serving diekspos melalui HTTPS. Prometheus dan Grafana disiapkan dalam image yang sama untuk menghindari kebutuhan service cloud tambahan. |
| Web app | **Model status:** [breast_cancer_model](https://mlops-dicoding-reza-production.up.railway.app/v1/models/breast_cancer_model)  •  **Metadata:** [serving metadata](https://mlops-dicoding-reza-production.up.railway.app/v1/models/breast_cancer_model/metadata)  •  endpoint prediksi: `POST https://mlops-dicoding-reza-production.up.railway.app/v1/models/breast_cancer_model:predict` |
| Monitoring | TensorFlow Serving mengekspor metric pada `/monitoring/prometheus/metrics`. Prometheus dikonfigurasi untuk melakukan scrape melalui **public cloud target** `https://mlops-dicoding-reza-production.up.railway.app/monitoring/prometheus/metrics`, bukan hostname internal/localhost. UI Prometheus dapat diakses pada [Targets](https://mlops-dicoding-reza-production-992b.up.railway.app/targets). Konfigurasi juga memuat `evaluation_interval`, `external_labels`, dan job-level `scrape_interval`. |

## Struktur Pipeline TFX

1. **CsvExampleGen** — membaca `data/breast_cancer.csv` dan menghasilkan TFRecord train/eval.
2. **StatisticsGen** — menghasilkan statistics protobuf dari examples.
3. **SchemaGen** — menghasilkan schema protobuf text.
4. **ExampleValidator** — menghasilkan hasil validasi/anomaly artifact.
5. **Transform** — menghasilkan transform graph serta transformed examples.
6. **Tuner** — mencari hyperparameter model.
7. **Trainer** — melatih dan mengekspor TensorFlow SavedModel.
8. **Resolver** — mengambil model terakhir yang telah diberkati sebagai baseline bila tersedia.
9. **Evaluator** — mengevaluasi model dengan Binary Accuracy dan AUC.
10. **Pusher** — menyalin model yang diberkati ke `serving_model/` untuk production serving.

## Menjalankan Proyek

Gunakan **Python 3.10** untuk kompatibilitas TFX 1.15.x.

```bash
pip install -r requirements.txt
python pipeline.py
```

Notebook `reza_harahap-pipeline.ipynb` mendokumentasikan inisialisasi komponen, pembangunan pipeline, eksekusi `BeamDagRunner`, dan verifikasi artifact. Notebook `reza_harahap-testing.ipynb` melakukan request langsung ke URL Railway sebenarnya dan harus disertakan bersama output hasil eksekusinya.

## Deployment dan Monitoring

Docker image menjalankan TensorFlow Serving pada port 8501, Prometheus pada 9090, dan Grafana pada 3000. Bukti deployment serta monitoring yang digunakan untuk review terdapat pada folder `evidence/cloud/` dan berasal dari endpoint cloud aktual. Prometheus submission config terdapat pada `monitoring/prometheus.yml`.
