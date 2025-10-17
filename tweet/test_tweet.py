import pytest
import requests
base_url = ""
def test_create_tweet():
    res = requests.post(f'{base_url}/tweet/create')
    data = res.json()
    assert res.status_code == 200
    assert data["status"] == "success"