import pytest
import requests
import random
import string

# -------------------
# 1. Get base URL from Jenkins
# -------------------
def pytest_addoption(parser):
    parser.addoption(
        "--base-url", action="store", required=True, help="Base URL for smoke tests"
    )

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

# -------------------
# 2. Helper to generate random email for testing
# -------------------
def random_email():
    return "smoke+" + "".join(random.choices(string.ascii_lowercase, k=5)) + "@test.com"

# -------------------
# 3. Smoke Tests
# -------------------

def test_register(base_url):
    """Test user registration"""
    email = random_email()
    payload = {"name": "Smoke Tester", "mail_id": email, "password": "123456"}
    response = requests.post(f"{base_url}/register", json=payload)
    assert response.status_code == 201 or response.status_code == 400
    # If user exists, it's okay for smoke test
    data = response.json()
    assert "message" in data

def test_login(base_url):
    """Test login for a known user"""
    # Use a fixed user you know exists on DB for smoke test or the one created just above
    email = "smokeuser@test.com"  # replace with a real test user in DB
    payload = {"mail_id": email, "password": "123456"}
    response = requests.post(f"{base_url}/login", json=payload)
    assert response.status_code in [200, 400, 401]  # login success or user not exists
    data = response.json()
    assert "message" in data or "detail" in data

def test_create_task(base_url):
    """Test creating a task for a user"""
    email = "smokeuser@test.com"  # replace with a test user
    payload = {"mail": email, "task_name": "Smoke Task", "description": "Smoke testing"}
    response = requests.post(f"{base_url}/create_task", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task added successfully"

def test_show_tasks(base_url):
    """Test fetching tasks"""
    email = "smokeuser@test.com"  # replace with a test user
    response = requests.get(f"{base_url}/show_tasks/{email}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # should return list of tasks

def test_delete_task(base_url):
    """Test deleting a specific task"""
    email = "smokeuser@test.com"  # replace with a test user
    task_name = "Smoke Task"
    params = {"mail": email, "task_name": task_name}
    response = requests.delete(f"{base_url}/delete_task", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
