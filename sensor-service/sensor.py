import random
import time
import logging
from collections import deque
from flask import Flask, jsonify

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# --------------------------------------------------
# Logging Setup
# --------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sensor-service")

# --------------------------------------------------
# Flask App
# --------------------------------------------------
app = Flask(__name__)

# --------------------------------------------------
# Custom Metrics
# --------------------------------------------------
REQUEST_COUNT = Counter(
    "sensor_requests_total",
    "Total number of requests received"
)

REQUEST_FAILURES = Counter(
    "sensor_failed_total",
    "Total number of failed requests"
)

QUEUE_DEPTH = Gauge(
    "sensor_queue_depth",
    "Simulated sensor processing queue depth"
)

CPU_SPIKE_DURATION = Histogram(
    "sensor_cpu_spike_seconds",
    "Duration of CPU spike simulation"
)

# --------------------------------------------------
# Internal State for Performance Simulation
# --------------------------------------------------
# bounded queue for lightweight memory behavior
processing_queue = deque(maxlen=500)


# --------------------------------------------------
# CPU Spike Logic (Bounded)
# --------------------------------------------------
def simulate_cpu_spike():
    """Simulates a bounded CPU spike and records its duration."""
    start_time = time.time()
    spike_duration = 0.15  # 150ms predictable spike

    while time.time() - start_time < spike_duration:
        pass  # controlled CPU burn

    CPU_SPIKE_DURATION.observe(time.time() - start_time)


# --------------------------------------------------
# Sensor Value Generator
# --------------------------------------------------
def generate_sensor_value():
    """Returns a synthetic sensor reading."""
    # Increase queue depth randomly (simulate load)
    current_depth = random.randint(0, 40)
    QUEUE_DEPTH.set(current_depth)

    # Add a lightweight entry to the internal bounded queue
    processing_queue.append(current_depth)

    # Introduce occasional CPU spikes
    if random.random() < 0.15:   # 15% chance
        simulate_cpu_spike()

    # Produce a sensor reading
    return round(random.uniform(20.0, 80.0), 2)


# --------------------------------------------------
# API Routes
# --------------------------------------------------
@app.route("/")
def get_sensor_value():
    """Main API returning sensor data."""
    REQUEST_COUNT.inc()

    try:
        value = generate_sensor_value()
        response = {"value": value}
        logger.info(f"Sensor reading returned: {value}")
        return jsonify(response), 200

    except Exception as e:
        REQUEST_FAILURES.inc()
        logger.error(f"Error while generating sensor value: {str(e)}")
        return jsonify({"error": "Sensor failure"}), 500


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# --------------------------------------------------
# Main Entrypoint
# --------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting Sensor Service on port 8000...")
    app.run(host="0.0.0.0", port=8000)
