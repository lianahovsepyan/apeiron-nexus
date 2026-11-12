import numpy as np
import json
from core.distributed_cluster_nexus import DistributedClusterNexus

print("🚀 Initializing Apeiron-Nexus Distributed Cluster...")
nodes = [f"node-compute-{i:03d}" for i in range(8)]
nexus = DistributedClusterNexus(cluster_nodes=nodes)

print("⚡ Executing Global Distributed Workload...")
test_data = np.random.normal(size=(128, 128))
result = nexus.execute_global_workload(test_data)
print(json.dumps(result, indent=4))
