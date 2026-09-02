#!/bin/bash
set -euo pipefail

/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --web.listen-address=0.0.0.0:9090 \
  --storage.tsdb.path=/tmp/prometheus-data &
PROM_PID=$!

/usr/bin/tensorflow_model_server \
  --rest_api_port=8501 \
  --model_name=breast_cancer_model \
  --model_base_path=/models/breast_cancer_model \
  --monitoring_config_file=/etc/tf_serving/prometheus.config &
TF_PID=$!

# Modern Grafana images keep the executable under /usr/share/grafana/bin.
# The whole /usr/share/grafana directory is copied in the Dockerfile.
/usr/share/grafana/bin/grafana server \
  --homepath=/usr/share/grafana \
  --config=/etc/grafana/grafana.ini &
GRAFANA_PID=$!

term_handler() {
  kill -TERM "$PROM_PID" "$TF_PID" "$GRAFANA_PID" 2>/dev/null || true
  wait "$PROM_PID" "$TF_PID" "$GRAFANA_PID" 2>/dev/null || true
}
trap term_handler TERM INT

wait -n "$PROM_PID" "$TF_PID" "$GRAFANA_PID"
EXIT_CODE=$?
term_handler
exit "$EXIT_CODE"
