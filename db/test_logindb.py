import pytest
import requests
def user():
    return {"username": "testuser","email":"testuser@gmail.com", "password": "testpass"}
def wrong_pass():
    return {"username": "testuser","email":"testuser@gmail.com", "password": "wrongpass"}
def wrong_user():
    return {"username": "wronguser","email":"testuser@gmail.com", "password": "testpass"}
   
def test_login_success(user):
    response = requests.post("/login", json=user)
    assert response.status_code == 200
    
def test_invalid_password(wrong_pass):
    response = requests.post("/login", json=wrong_pass)
    assert response.status_code == 401
    
def test_invalid_username(wrong_user):
    response = requests.post("/login", json=wrong_user)
    assert response.status_code == 402
    
def test_user_not_found():
    response = requests.post("/login", json={})
    assert response.status_code == 400