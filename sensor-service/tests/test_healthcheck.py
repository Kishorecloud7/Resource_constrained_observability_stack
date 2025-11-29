import requests

def test_root_endpoint():
    response = requests.get("http://localhost:8000/")
    
    # Check API reachable
    assert response.status_code == 200
    
    # Response must contain a JSON with a "value" field
    data = response.json()
    assert "value" in data
    assert isinstance(data["value"], float)
