import pytest
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_register():
    response=client.post("/register",json={"name":"test_user","mail_id":"test@gmail.com","password":"testpass"})
    assert "message" in response.json()
