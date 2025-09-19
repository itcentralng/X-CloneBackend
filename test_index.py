import pytest, requests


def test_status():
    res = requests.get("http://127.0.0.1:5000/status")
    assert res.status_code == 200