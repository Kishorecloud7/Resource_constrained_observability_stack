import requests

def test_root_endpoint():
    """Test that the root sensor endpoint returns a valid response."""
    response = requests.get("http://localhost:8000/")

    # Service must be reachable
    assert response.status_code == 200

    data = response.json()

    # Response must include the sensor value
    assert "value" in data
    assert isinstance(data["value"], (float, int))
