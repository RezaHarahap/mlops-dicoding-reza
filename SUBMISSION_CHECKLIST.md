# Submission Checklist

## Kriteria wajib — source/package
- [x] Source pipeline TFX lengkap: ExampleGen, StatisticsGen, SchemaGen, ExampleValidator, Transform, Tuner, Trainer, Resolver, Evaluator, Pusher
- [x] Apache Beam (`BeamDagRunner`)
- [x] Folder `reza_harahap-pipeline`
- [x] Notebook dokumentasi tersedia
- [x] Python modules, `requirements.txt`, dan Markdown
- [x] Dockerfile TensorFlow Serving
- [x] Monitoring config TensorFlow Serving (`prometheus.config`)
- [x] Folder monitoring + Dockerfile + `prometheus.yml`
- [x] Grafana provisioning + dashboard JSON
- [x] Notebook prediction request
- [x] Railway deployment config

## Bukti runtime yang harus nyata
- [ ] `reza_harahap-deployment.png`
- [ ] `reza_harahap-monitoring.png`
- [ ] `reza_harahap-pylint.png`
- [ ] `reza_harahap-grafana-dashboard.png` (untuk saran Grafana)

## Smoke test paket yang sudah tersedia
- Dataset rows: 569
- AUC baseline: 0.9954
- Binary Accuracy baseline: 0.9825
- Python syntax check: PASS

## Catatan penting
Folder `serving_model/` adalah target TFX Pusher. SavedModel nyata harus dihasilkan dari eksekusi pipeline sebelum deployment cloud. Bukti cloud/monitoring tidak boleh disintesis.
