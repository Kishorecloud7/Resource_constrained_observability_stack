import requests

def test_metrics_endpoint():
    # Check that the metrics endpoint is reachable
    response = requests.get("http://localhost:8001/metrics")
    
    assert response.status_code == 200
    assert "sensor_requests_total" in response.text
    assert "sensor_failed_total" in response.text
    assert "sensor_queue_depth" in response.text
    assert "sensor_cpu_spike_seconds" in response.text
