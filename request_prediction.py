"""Send a prediction request to TensorFlow Serving."""
import json
import os

import pandas as pd
import requests

BASE_URL = os.getenv(
    "MODEL_BASE_URL",
    "http://localhost:8501",
).rstrip("/")
URL = f"{BASE_URL}/v1/models/breast_cancer_model:predict"

features = (
    pd.read_csv("data/breast_cancer.csv")
    .drop(columns=["label"])
    .iloc[0]
    .astype("float32")
    .tolist()
)

payload = {"instances": [features]}
response = requests.post(URL, json=payload, timeout=30)
response.raise_for_status()
print(json.dumps(response.json(), indent=2))
