import pytest
import requests
import os
from dotenv import load_dotenv
load_dotenv('../.env')
base_url = os.getenv("BASE_URL")

def test_create_tweet():
    login_payload = {"username": "atto", "password": "your_password_here"}
    login_res = requests.post(f'{base_url}/login', json=login_payload)
    assert login_res.status_code == 200
    token = login_res.json().get("token")
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"username":"atto","tweeting":"This is the first Tweet Test"}
    res = requests.post(f'{base_url}/tweet/create', json=payload, headers=headers)
    data = res.json()
    assert res.status_code == 200
    assert data["Post"]