# Deployment & Evidence Checklist

Dokumen ini adalah panduan eksekusi terakhir untuk menghasilkan bukti yang **harus berasal dari runtime nyata**.

## 1. Jalankan pipeline TFX
Gunakan Python 3.10 dan environment baru.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python pipeline.py
```

Pastikan `serving_model/` berisi SavedModel hasil `Pusher` yang di-bless.

## 2. Verifikasi lokal

```bash
docker compose up --build
```

Endpoint model:
- REST: `http://localhost:8501/v1/models/breast_cancer_model`
- Prometheus metrics: `http://localhost:8501/monitoring/prometheus/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## 3. Deployment cloud
Deploy root project memakai Dockerfile ke Railway/Render/platform container cloud lain. Setelah endpoint publik aktif, isi URL pada README dan notebook testing.

## 4. Bukti yang wajib disimpan
- `reza_harahap-deployment.png` — endpoint/model serving cloud aktif.
- `reza_harahap-monitoring.png` — dashboard/targets Prometheus menunjukkan service UP.
- `reza_harahap-pylint.png` — hasil pylint terhadap folder `modules`.
- `reza_harahap-grafana-dashboard.png` — dashboard Grafana bila mengejar saran keempat.

Jangan gunakan screenshot sintetis. Bukti reviewer harus berasal dari eksekusi nyata.
