import json
from core.task_broker import ApeironTaskBroker

print("🚀 Initializing Apeiron-Nexus Task Broker...")
broker = ApeironTaskBroker()

print("📥 Dispatching High-Priority Quantum Tasks...")
t1 = broker.submit_task("tensor_contraction", {"qubits": 20}, priority=1)
t2 = broker.submit_task("svd_compression", {"matrix_size": 256}, priority=2)
t3 = broker.submit_task("grape_pulse_optimization", {"controls": 8}, priority=1)

print(f"Tasks submitted successfully. Queue length: 3")

print("\n⚡ Processing Tasks via Cluster Workers...")
print(json.dumps(broker.process_queue("node-compute-000"), indent=4))
print(json.dumps(broker.process_queue("node-compute-001"), indent=4))
print(json.dumps(broker.process_queue("node-compute-002"), indent=4))
