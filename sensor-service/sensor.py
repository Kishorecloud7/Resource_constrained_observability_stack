import time
import threading
import random
from collections import deque

from prometheus_client import (
    start_http_server,
    Counter,
    Gauge,
    Histogram
)
import psutil
from flask import Flask, jsonify

app = Flask(__name__)

# -------------------------
# Metrics
# -------------------------
REQUESTS = Counter("sensor_requests_total", "Total sensor requests")
FAILURES = Counter("sensor_failed_total", "Total failed requests")
QUEUE_DEPTH = Gauge("sensor_queue_depth", "Current buffer depth")

CPU_SPIKE_DURATION = Histogram(
    "sensor_cpu_spike_seconds",
    "Duration of CPU spikes in seconds",
    buckets=[0.1, 0.5, 1, 2, 5, 10]
)

# Bounded buffer to prevent memory spikes
buffer = deque(maxlen=500)

# -------------------------
# CPU Spike Monitor (Background Thread)
# -------------------------
def cpu_spike_monitor():
    last_high = None
    while True:
        cpu = psutil.cpu_percent(interval=0.5)

        # Detect spike start
        if cpu > 60:
            if last_high is None:
                last_high = time.time()

        # Spike ended → record duration
        else:
            if last_high:
                duration = time.time() - last_high
                CPU_SPIKE_DURATION.observe(duration)
                last_high = None

        time.sleep(0.2)

# -------------------------
# Metrics Server (Runs independently)
# -------------------------
def metrics_server():
    start_http_server(8001)
    print("Metrics available at http://localhost:8001/metrics")

# -------------------------
# Main API Endpoint
# -------------------------
@app.get("/")
def root():
    try:
        REQUESTS.inc()

        # Simulated sensor reading
        value = random.random()

        buffer.append(value)
        QUEUE_DEPTH.set(len(buffer))

        return jsonify({"value": value})

    except Exception:
        FAILURES.inc()
        return jsonify({"error": "internal failure"}), 500

# -------------------------
# Application Entry Point
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=cpu_spike_monitor, daemon=True).start()
    threading.Thread(target=metrics_server, daemon=True).start()

    app.run(host="0.0.0.0", port=8000)
