from core.nvidia_cuda_bridge import NVIDIAHardwareBridge
import numpy as np

bridge = NVIDIAHardwareBridge()
my_huge_tensor = np.random.normal(size=100)
result = bridge.accelerate_tensor_contraction(my_huge_tensor)

print("🚀 NVIDIA Hardware Bridge Test Result:")
print(result)
