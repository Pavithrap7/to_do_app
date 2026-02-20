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
    response=client.post("/login",json={"mail_id":"test@gmail.com","password":"test123"})
    assert "detail" in response.json()

def test_login_invalid_username():
    response=client.post("/login",json={"mail_id":"test1@gmail.com","password":"testpass"})
    assert "detail" in response.json()

def test_create_task_without_description():
    response=client.post("/create_task",json={"mail":"test@gmail.com","task_name":"test_task1"})
    assert "message" in response.json()

def test_create_task_with_description():
    response=client.post("/create_task",json={"mail":"test@gmail.com","task_name":"test_task2","description":"this is about creating tasks"})
    assert "message" in response.json()

    
