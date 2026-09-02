FROM grafana/grafana:latest AS grafana
FROM prom/prometheus:latest AS prometheus
FROM tensorflow/serving:2.15.1

USER root

ENV MODEL_NAME=breast_cancer_model
ENV MODEL_BASE_PATH=/models/breast_cancer_model
ENV GF_PATHS_HOME=/usr/share/grafana
ENV GF_PATHS_CONFIG=/etc/grafana/grafana.ini
ENV GF_PATHS_DATA=/tmp/grafana-data
ENV GF_PATHS_LOGS=/tmp/grafana-logs
ENV GF_PATHS_PLUGINS=/tmp/grafana-plugins
ENV GF_PATHS_PROVISIONING=/etc/grafana/provisioning
ENV GF_SECURITY_ADMIN_USER=admin
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false
ENV GF_SERVER_HTTP_PORT=3000

COPY --from=prometheus /bin/prometheus /usr/local/bin/prometheus
COPY --from=prometheus /bin/promtool /usr/local/bin/promtool
COPY --from=grafana /usr/share/grafana /usr/share/grafana

COPY serving_model /models/breast_cancer_model
COPY monitoring/prometheus.config /etc/tf_serving/prometheus.config
COPY monitoring/prometheus.single-service.yml /etc/prometheus/prometheus.yml
COPY monitoring/grafana/provisioning /etc/grafana/provisioning
COPY monitoring/grafana/dashboards /var/lib/grafana/dashboards
COPY start-services.sh /usr/local/bin/start-services.sh

RUN mkdir -p /tmp/grafana-data /tmp/grafana-logs /tmp/grafana-plugins /etc/grafana && \
    printf '[server]\nhttp_addr = 0.0.0.0\nhttp_port = 3000\n[security]\nadmin_user = admin\nadmin_password = admin\n[users]\nallow_sign_up = false\n' > /etc/grafana/grafana.ini && \
    chmod +x /usr/local/bin/start-services.sh

EXPOSE 3000 8501 9090

ENTRYPOINT ["/usr/local/bin/start-services.sh"]
