import json
import time
from core.distributed_telemetry_streamer import TelemetryStreamer

print("📡 Initializing Apeiron-Nexus Real-Time Telemetry Streamer...")
nodes = [f"node-compute-{i:03d}" for i in range(4)]
streamer = TelemetryStreamer(nodes)

print("🔄 Simulating 3 Live Telemetry Ticks...")
for i in range(3):
    metric_tick = streamer.stream_metrics_tick()
    print(f"\n--- Tick {i+1} ---")
    print(json.dumps(metric_tick, indent=4))
    time.sleep(0.5)
