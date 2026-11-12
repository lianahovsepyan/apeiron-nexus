import requests
import json

url = "http://127.0.0.1:8000/v1/cluster/execute"
payload = {
    "qubits": 16,
    "nodes": 4,
    "depth": 20
}

response = requests.post(url, json=payload)
print("🌐 Distributed Cluster Execution Results:")
print(json.dumps(response.json(), indent=4))
