import requests

def test_metrics_endpoint():
    """Test that the /metrics endpoint exposes required custom metrics."""
    response = requests.get("http://localhost:8000/metrics")

    # Endpoint must return OK
    assert response.status_code == 200

    metrics = response.text

    # Verify presence of expected custom metrics
    assert "sensor_requests_total" in metrics
    assert "sensor_failed_total" in metrics
    assert "sensor_queue_depth" in metrics
    assert "sensor_cpu_spike_seconds" in metrics
