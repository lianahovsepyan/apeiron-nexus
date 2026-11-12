import requests
import json

url = "http://127.0.0.1:8000/v1/mitigate-errors"
payload = {
    "qubits": 4,
    "scale_factors": [1.0, 2.0, 4.0]
}

response = requests.post(url, json=payload)
print("🛡️ Zero-Noise Extrapolation Results:")
print(json.dumps(response.json(), indent=4))
