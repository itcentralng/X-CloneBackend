import pytest
import requests
base_url = "http://127.0.0.1:5000"
payload = {"username":"atto","tweeting":"This is the first Tweet Test"}
def test_create_tweet():
    res = requests.post(f'{base_url}/tweet/create',json=payload)
    data = res.json()
    print(data)
    assert res.status_code == 200
    assert data["Post"]