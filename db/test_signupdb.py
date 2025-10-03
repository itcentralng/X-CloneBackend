import pytest
import requests
def user():
    return {"username": "testuser","email":"testuser@gmail.com", "password": "testpass"}
def test_success(user):
    response = requests.post("/signup", json=user)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
def test_missing_field():
    response = requests.post("/signup", json={"username": "testuser"})
    assert response.status_code == 500
def test_invalid_data_type():
    response = requests.post("/signup", json={"username": 123, "email":""})
    assert response.status_code == 500
def test_empty_payload():
    response = requests.post("/signup", json={})
    assert response.status_code == 500