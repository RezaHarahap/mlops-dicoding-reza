"""Send a serialized tf.Example prediction request to TensorFlow Serving."""
import base64
import json
import os

import pandas as pd
import requests
import tensorflow as tf

BASE_URL = os.getenv(
    "MODEL_BASE_URL",
    "https://mlops-dicoding-reza-production.up.railway.app",
).rstrip("/")
MODEL_NAME = "breast_cancer_model"
URL = f"{BASE_URL}/v1/models/{MODEL_NAME}:predict"

row = pd.read_csv("data/breast_cancer.csv").drop(columns=["label"]).iloc[0]
feature_map = {
    str(name): tf.train.Feature(
        float_list=tf.train.FloatList(value=[float(value)])
    )
    for name, value in row.items()
}
example = tf.train.Example(
    features=tf.train.Features(feature=feature_map)
)
serialized_b64 = base64.b64encode(
    example.SerializeToString()
).decode("ascii")

payload = {
    "instances": [
        {"examples": {"b64": serialized_b64}}
    ]
}

print("POST", URL)
print("Payload format: serialized tf.Example -> Base64 -> instances[0].examples.b64")
response = requests.post(URL, json=payload, timeout=60)
print("HTTP status:", response.status_code)
print(json.dumps(response.json(), indent=2))
response.raise_for_status()
