import requests
import json

url = "http://127.0.0.1:8000/v1/qml/optimize"
payload = {
    "qubits": 4,
    "initial_params": [0.1, 0.5, 1.2, 0.8],
    "iterations": 30
}

response = requests.post(url, json=payload)
print("🧬 QML & VQE Ground-State Optimization Results:")
print(json.dumps(response.json(), indent=4))
