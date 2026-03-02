import pytest
from fastapi.testclient import TestClient
from app.main import app
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# Logging wrapper for TestClient
class LoggingClient:
    def __init__(self, client):
        self.client = client

    def post(self, url, **kwargs):
        logging.debug(f"POST {url} with payload: {kwargs.get('json')}")
        response = self.client.post(url, **kwargs)
        logging.debug(f"Response {response.status_code}: {response.json()}")
        return response

    def get(self, url, **kwargs):
        logging.debug(f"GET {url} with params: {kwargs.get('params')}")
        response = self.client.get(url, **kwargs)
        logging.debug(f"Response {response.status_code}: {response.json()}")
        return response

    def delete(self, url, **kwargs):
        logging.debug(f"DELETE {url} with payload: {kwargs.get('json')}")
        response = self.client.delete(url, **kwargs)
        logging.debug(f"Response {response.status_code}: {response.json()}")
        return response


# Use LoggingClient for all tests
client = LoggingClient(TestClient(app))
#client=TestClient(app)

#def test_register():
#    response=client.post("/register",json={"name":"test_user","mail_id":"test@gmail.com","password":"testpass"})
#    assert "message" in response.json()

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


def test_show_tasks():
    # Create a task first
    client.post("/create_task", json={
        "mail": "test@gmail.com",
        "task_name": "test_task2",
        "description": "this is about creating tasks"
    })

    # Fetch tasks for the user
    response = client.get("/show_tasks/test@gmail.com")
    tasks = response.json()

    # Assert that the response is a list and contains the task we just created
    assert isinstance(tasks, list)
    assert any(task["name"] == "test_task2" for task in tasks)


def test_del_tasks():
    mail = "test@gmail.com"

    # Create some tasks first
    client.post("/create_task", json={"mail": mail, "task_name": "task_a", "description": "desc a"})
    client.post("/create_task", json={"mail": mail, "task_name": "task_b", "description": "desc b"})

    # Delete a single task (task_a)
    response = client.delete(f"/delete_task?mail={mail}&task_name=task_a")
    assert response.status_code == 200
    assert response.json()["message"] == "Task 'task_a' deleted for test@gmail.com"

    # Verify only task_b remains
    tasks = client.get(f"/show_tasks/{mail}").json()
    assert isinstance(tasks, list)
    task_names = [t["name"] for t in tasks]
    assert "task_a" not in task_names
    assert "task_b" in task_names

    # Delete all remaining tasks for the user
    response = client.delete(f"/delete_task?mail={mail}")
    assert response.status_code == 200
    assert response.json()["message"] == f"All tasks deleted for {mail}"

    # Verify tasks are empty
    tasks = client.get(f"/show_tasks/{mail}").json()
    assert isinstance(tasks, list)
    assert tasks == []
