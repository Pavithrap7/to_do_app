import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_register():
    response=client.post("/register",json={"name":"test_user","mail_id":"test@gmail.com","password":"testpass"})
    assert "message" in response.json()

def test_login_correct_password():
    response=client.post("/login",json={"mail_id":"test@gmail.com","password":"testpass"})
    assert "message" in response.json()

def test_login_incorrect_password():
    response=client.post("/login",json={"mail_id":"tes1t@gmail.com","password":"test123"})
    assert "detail" in response.json()

def test_login_invalid_username():
    response=client.post("/login",json={"name":"123","mail_id":"test@gmail.com","password":"testpass"})
    assert "detail" in response.json()
