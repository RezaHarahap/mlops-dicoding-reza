"""Send a prediction request to TensorFlow Serving."""
import json, requests, pandas as pd
URL='http://localhost:8501/v1/models/breast_cancer_model:predict'
row=pd.read_csv('data/breast_cancer.csv').drop(columns=['label']).iloc[0].to_dict()
payload={'instances':[row]}
response=requests.post(URL,json=payload,timeout=30)
response.raise_for_status()
print(json.dumps(response.json(),indent=2))
