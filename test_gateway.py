import json
from core.api_gateway import ApeironApiGateway

print("🚀 Initializing Apeiron-Nexus API Gateway...")
gateway = ApeironApiGateway()

print("\n📡 Testing Endpoint: /api/v1/compress")
res1 = gateway.route_request("/api/v1/compress", {"size": 32})
print(json.dumps(res1, indent=4))

print("\n📡 Testing Endpoint: /api/v1/grape")
res2 = gateway.route_request("/api/v1/grape", {})
print(json.dumps(res2, indent=4))

print("\n📡 Testing Endpoint: /api/v1/task/submit & process")
t_res = gateway.route_request("/api/v1/task/submit", {"task_type": "deep_contraction", "priority": 1})
print(json.dumps(t_res, indent=4))
process_res = gateway.route_request("/api/v1/task/process", {"worker": "node-compute-007"})
print(json.dumps(process_res, indent=4))
