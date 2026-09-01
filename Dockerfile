FROM prom/prometheus:latest AS prometheus

FROM tensorflow/serving:2.15.1

USER root

ENV MODEL_NAME=breast_cancer_model
ENV MODEL_BASE_PATH=/models/breast_cancer_model

COPY --from=prometheus /bin/prometheus /usr/local/bin/prometheus
COPY --from=prometheus /bin/promtool /usr/local/bin/promtool
COPY serving_model /models/breast_cancer_model
COPY monitoring/prometheus.config /etc/tf_serving/prometheus.config
COPY monitoring/prometheus.single-service.yml /etc/prometheus/prometheus.yml
COPY start-services.sh /usr/local/bin/start-services.sh

RUN chmod +x /usr/local/bin/start-services.sh

EXPOSE 8501 9090

ENTRYPOINT ["/usr/local/bin/start-services.sh"]
