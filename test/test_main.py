import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        json={"name":"test_user","mail_id":"test@gmail.com","password":"testpass"}
    )
    assert "message" in response.json()
    assert response.status_code in [201, 400]  # 400 if test user already exists

def test_login_fail():
    response = client.post(
        "/login",
        json={"mail_id":"nonexist@gmail.com","password":"wrongpass"}
    )
    assert response.status_code == 400 or response.status_code == 401

def test_create_task():
    response = client.post(
        "/create_task",
        json={"mail":"test@gmail.com","task_name":"task1","description":"desc"}
    )
    assert "message" in response.json()

