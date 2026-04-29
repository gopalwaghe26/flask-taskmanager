import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200

def test_create_task(client):
    payload = {"title": "Test task", "priority": "high"}
    response = client.post('/tasks',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test task'
    assert 'id' in data

def test_create_task_no_title(client):
    response = client.post('/tasks',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400

def test_get_single_task(client):
    payload = {"title": "Find me"}
    create_resp = client.post('/tasks',
                              data=json.dumps(payload),
                              content_type='application/json')
    task_id = json.loads(create_resp.data)['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200

def test_update_task(client):
    payload = {"title": "Original"}
    create_resp = client.post('/tasks',
                              data=json.dumps(payload),
                              content_type='application/json')
    task_id = json.loads(create_resp.data)['id']
    update = {"title": "Updated", "status": "done"}
    response = client.put(f'/tasks/{task_id}',
                          data=json.dumps(update),
                          content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['title'] == 'Updated'

def test_delete_task(client):
    payload = {"title": "Delete me"}
    create_resp = client.post('/tasks',
                              data=json.dumps(payload),
                              content_type='application/json')
    task_id = json.loads(create_resp.data)['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200

def test_get_nonexistent_task(client):
    response = client.get('/tasks/does-not-exist')
    assert response.status_code == 404
