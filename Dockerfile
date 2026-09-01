FROM tensorflow/serving:2.15.1

ENV MODEL_NAME=breast_cancer_model
ENV MODEL_BASE_PATH=/models/breast_cancer_model

COPY serving_model /models/breast_cancer_model
COPY monitoring/prometheus.config /etc/tf_serving/prometheus.config

EXPOSE 8501

ENTRYPOINT ["/usr/bin/tensorflow_model_server"]
CMD ["--rest_api_port=8501", "--model_name=breast_cancer_model", "--model_base_path=/models/breast_cancer_model", "--monitoring_config_file=/etc/tf_serving/prometheus.config"]
