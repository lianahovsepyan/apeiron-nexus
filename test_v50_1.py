import requests

url = "http://127.0.0.1:8000/api/v1/execute"
payload = {
    "gates": ["H0", "CNOT0,1"],
    "qubits": 4,
    "noise_enabled": True,
    "topological_nullification": True,
    "chronos_time_steps": 5
}

try:
    response = requests.post(url, json=payload)
    print("--- v50.1 Scientific Validation Response ---")
    print(response.json())
except requests.exceptions.ConnectionError:
    print("[!] Local server is not running. Start it with: python main.py")
