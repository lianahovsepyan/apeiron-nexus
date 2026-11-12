import json
from core.quantum_optimal_control import QuantumOptimalControlEngine
from core.hyper_tensor_network import HyperTensorContractionEngine

print("⚡ Running Quantum Optimal Control (GRAPE) Engine...")
grape = QuantumOptimalControlEngine(num_controls=4, time_steps=40)
grape_res = grape.optimize_pulses()
print(json.dumps(grape_res, indent=4))

print("\n🌐 Running Hyper-Graph Tensor Contraction Engine...")
hyper = HyperTensorContractionEngine(network_size=64)
hyper_res = hyper.compute_optimal_path()
print(json.dumps(hyper_res, indent=4))
