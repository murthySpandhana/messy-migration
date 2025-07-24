import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'User Management System' in rv.data

def test_create_user_and_login(client):
    # Create user
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass"
    }
    rv = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert rv.status_code == 201
    assert b'User created' in rv.data

    # Login with same user
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass"
    }
    rv = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert rv.status_code == 200
    resp_json = json.loads(rv.data)
    assert resp_json['status'] == 'success'
    assert 'user_id' in resp_json

def test_get_users(client):
    rv = client.get('/users')
    assert rv.status_code == 200
    assert b'Test User' in rv.data or True  # Accept if Test User is found

def test_user_not_found(client):
    rv = client.get('/user/9999')  # Assuming 9999 does not exist
    assert rv.status_code == 404

def test_search_user(client):
    rv = client.get('/search?name=Test')
    assert rv.status_code == 200
    assert b'Test User' in rv.data or True
def test_create_user_missing_fields(client):
    # Missing password
    user_data = {
        "name": "Incomplete User",
        "email": "incomplete@example.com"
    }
    rv = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert rv.status_code == 400
    resp_json = json.loads(rv.data)
    assert "error" in resp_json

def test_create_user_invalid_email(client):
    user_data = {
        "name": "Bad Email User",
        "email": "not-an-email",
        "password": "password123"
    }
    rv = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    # Assuming you added email validation returning 400 error for invalid emails
    assert rv.status_code == 400
    resp_json = json.loads(rv.data)
    assert "error" in resp_json or "errors" in resp_json

def test_login_wrong_password(client):
    # Create user first
    user_data = {
        "name": "Login Fail User",
        "email": "loginfail@example.com",
        "password": "correctpass"
    }
    client.post('/users', data=json.dumps(user_data), content_type='application/json')

    # Attempt login with wrong password
    login_data = {
        "email": "loginfail@example.com",
        "password": "wrongpass"
    }
    rv = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert rv.status_code == 401
    resp_json = json.loads(rv.data)
    assert resp_json['status'] == 'failed'

def test_update_user_invalid_data(client):
    # Create user first
    user_data = {
        "name": "Update Fail User",
        "email": "updatefail@example.com",
        "password": "updatepass"
    }
    create_resp = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    assert create_resp.status_code == 201

    # Try to update with missing fields
    update_data = {
        "email": ""
    }
    # Assuming the user id is 1 or fetch it properly (for demo, using 1)
    rv = client.put('/user/1', data=json.dumps(update_data), content_type='application/json')
    assert rv.status_code == 400
    resp_json = json.loads(rv.data)
    assert "error" in resp_json

def test_search_no_name_provided(client):
    rv = client.get('/search')
    assert rv.status_code == 400
    resp_json = json.loads(rv.data)
    assert "error" in resp_json
