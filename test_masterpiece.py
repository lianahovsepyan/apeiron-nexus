import numpy as np
from core.tensor_compression import TensorCompressionEngine
from core.fault_tolerant_scheduler import FaultTolerantScheduler

print("🔬 Testing Tensor Compression Engine...")
compressor = TensorCompressionEngine(threshold=1e-3)
huge_tensor = np.random.normal(size=(64, 64))
compression_res = compressor.compress_tensor_network(huge_tensor)
print(compression_res)

print("\n🛡️ Testing Fault-Tolerant Cluster Scheduler...")
nodes = [f"node-compute-{i:03d}" for i in range(8)]
scheduler = FaultTolerantScheduler(nodes)
health_status = scheduler.simulate_node_health_check()
import json
print(json.dumps(health_status, indent=4))
