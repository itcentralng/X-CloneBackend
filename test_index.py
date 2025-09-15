import pytest, requests

response = requests.get("/status")
def test_status():
    assert response['status'] == "OK"
    assert response['version'] == "1.0"
    assert "uptime" in response
    assert "timestamp" in response