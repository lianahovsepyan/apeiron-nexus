import requests
import json

# API Endpoint URL
url = "http://127.0.0.1:8000/v1/simulate"

# Payload representing the autonomous scientific objective
payload = {
    "objective": "maximize_entanglement",
    "qubits": 4,
    "parameters": {
        "theta": 1.57079632679  # pi / 2
    }
}

headers = {
    "Content-Type": "application/json"
}

print("🚀 Sending autonomous request to Apeiron-Nexus Engine...")
response = requests.post(url, data=json.dumps(payload), headers=headers)

if response.status_code == 200:
    print("\n✅ Simulation Successfully Completed by Apeiron-Nexus!")
    result = response.json()
    print(json.dumps(result, indent=4))
else:
    print(f"\n❌ Error {response.status_code}:", response.text)
