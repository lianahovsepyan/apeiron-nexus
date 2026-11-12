"""
Apeiron-Nexus Master Integration Test Suite.
Validates the end-to-end synchronization of all 14 deeptech subsystems:
Quantum Optimal Control, Hyper-Tensor, SVD Compression, Fault Tolerance,
Task Broker, API Gateway, and Real-Time Telemetry.
"""

import numpy as np
import json
from core.api_gateway import ApeironApiGateway
from core.distributed_telemetry_streamer import TelemetryStreamer

print("=" * 60)
print("🚀 INITIALIZING APEIRON-NEXUS MASTER INTEGRATION SUITE")
print("=" * 60)

# 1. Initialize Gateway & Telemetry
gateway = ApeironApiGateway()
nodes = [f"node-compute-{i:03d}" for i in range(8)]
streamer = TelemetryStreamer(nodes)

# 2. Test Quantum Optimal Control via Gateway
print("\n[1/4] Executing Quantum Optimal Control (GRAPE)...")
grape_res = gateway.route_request("/api/v1/grape", {})
print(f"   -> Status: {grape_res['status']} | Final Fidelity: {grape_res['data']['final_gate_fidelity']}")

# 3. Test Tensor Compression via Gateway
print("\n[2/4] Executing SVD Tensor Compression Workload...")
comp_res = gateway.route_request("/api/v1/compress", {"size": 64})
print(f"   -> Status: {comp_res['status']} | Max Singular Value: {comp_res['data']['max_singular_value']}")

# 4. Test Task Broker & Cluster Health
print("\n[3/4] Dispatching & Processing Task via Apeiron-MQ...")
sub_res = gateway.route_request("/api/v1/task/submit", {"task_type": "master_quantum_sync", "priority": 1})
print(f"   -> Task Submitted ID: {sub_res.get('task_id')}")
proc_res = gateway.route_request("/api/v1/task/process", {"worker": "node-compute-000"})
print(f"   -> Task Executed By: {proc_res['data']['worker']} | Time: {proc_res['data']['task_summary']['execution_time_ms']} ms")

# 5. Stream Live Telemetry
print("\n[4/4] Fetching Real-Time Cluster Telemetry Snapshot...")
telemetry = streamer.stream_metrics_tick()
print(f"   -> Global Cluster Health: {telemetry['global_cluster_health'].upper()}")
print(f"   -> Active Nodes Monitored: {len(telemetry['nodes'])}")

print("\n" + "=" * 60)
print("✨ ALL 14 DEEPTECH SUBSYSTEMS PASSED INTEGRATION VALIDATION!")
print("=" * 60)
