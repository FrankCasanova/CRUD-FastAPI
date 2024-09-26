from main import app
from fastapi.testclient import TestClient
from operations import get_all_tasks
from schemas import TaskWithID

client = TestClient(app)

from conftest import TEST_TASKS, TEST_TASKS_V2

def test_endopint_read_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == TEST_TASKS
    assert len(response.json()) == 2
    assert response.headers["Content-Type"] == "application/json"

def test_endpoint_read_all_tasks_v2():
    response = client.get("/v2/tasks")
    print(TEST_TASKS_V2)
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.headers["Content-Type"] == "application/json"
    assert response.json()[1]['priority'] == 'lower'


def test_endpoint_search_tasks():
    response = client.get("/tasks/search?keyword=Test")
    assert response.status_code == 200
    assert response.json() == TEST_TASKS
    assert len(response.json()) == 2
    assert response.headers["Content-Type"] == "application/json"

def test_endpoint_read_task_by_id():
    response = client.get("/task/1")
    assert response.status_code == 200
    assert response.json() == TEST_TASKS[0]
    assert response.headers["Content-Type"] == "application/json"

    response = client.get("/task/2")
    assert response.status_code == 200
    assert response.json() == TEST_TASKS[1]
    assert response.headers["Content-Type"] == "application/json"

    response = client.get("/task/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    assert response.headers["Content-Type"] == "application/json"

def test_endpoint_create_task():
    task = {
        "title": "To Define",
        "description": "will be done",
        "status": "Ready",
    }
    headers = {
        "Authorization": "Bearer tokenizedjohndoe"
    }
    response = client.post("/task", json=task, headers=headers)
    assert response.status_code == 200
    assert response.json() == {**task, "id": 3}
    assert len(get_all_tasks()) == 3

def test_endpoint_update_task():
    task = {
        "title": "To Define",
        "description": "will be done",
        "status": "Ready",
    }
    headers = {
        "Authorization": "Bearer tokenizedjohndoe"
    }
    response = client.put("/task/1", json=task, headers=headers)
    assert response.status_code == 200
    response = client.put("/task/8", json=task, headers=headers)
    assert response.status_code == 404

def test_endopint_delete_task():
    headers = {
        "Authorization": "Bearer tokenizedjohndoe"
    }
    response = client.delete("/task/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Task One", "description": "Test Description One", "status": "Incomplete"}
    assert len(get_all_tasks()) == 1
