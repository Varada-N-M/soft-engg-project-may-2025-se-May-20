import json
import uuid
from datetime import date

import pytest
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash

from api.auth.routes import Login
from backend.app import create_app, db
from models import Child, UserRole, Users, GratitudeEntries

from datetime import datetime, timezone


import pytest
from flask_jwt_extended import create_access_token
from datetime import datetime

#1. Test create gratitude entry
def test_create_gratitude_entry(client, child_user):
    # child_user fixture returns (user, child)
    user, child = child_user

    # Create a valid JWT access token using the user's ID
    access_token = create_access_token(identity=str(user.user_id))

    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'gratitude_text': 'I am grateful for my parents'}

    response = client.post('/api/child/gratitude', json=payload, headers=headers,content_type='application/json')

    print("Request payload:", payload)
    print("Request headers:", headers)
    print("Response status:", response.status_code)
    print("Response JSON:", response.get_json())

    assert response.status_code == 201
    data = response.get_json()
    assert data['gratitude_text'] == payload['gratitude_text']
    assert 'entry_id' in data
    assert 'created_at' in data




# 2. Test creation fails with missing text
def test_create_gratitude_entry_no_text(client, child_user):

    # child_user fixture returns (user, child)
    user, child = child_user
    # Create a valid JWT access token using the user's ID
    access_token = create_access_token(identity=str(user.user_id))

    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/child/gratitude', headers=headers, json={},content_type='application/json')
    assert response.status_code == 400
    assert response.get_json().get('error')


# 3. Test retrieval of all gratitude entries
def test_get_all_gratitude_entries(client, auth_header):
    client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'Grateful for sunshine'},content_type='application/json')
    response = client.get('/api/child/gratitude', headers=auth_header,content_type='application/json')
    assert response.status_code == 200
    assert isinstance(response.get_json().get('entries'), list)


# 4. Test retrieval by specific date
def test_get_gratitude_entries_by_date(client, auth_header):
    client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'Today is special'})
    today = datetime.utcnow().strftime("%d-%m-%y")
    response = client.get(f'/api/child/gratitude?date={today}', headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.get_json().get('entries'), list)


# 5. Test retrieval by number of days
def test_get_gratitude_entries_by_days(client, auth_header):
    client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'Grateful for food'})
    response = client.get('/api/child/gratitude?days=2', headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.get_json().get('entries'), list)


# 6. Test invalid date format
def test_get_gratitude_entries_invalid_date_format(client, auth_header):
    response = client.get('/api/child/gratitude?date=2024-01-01', headers=auth_header)
    assert response.status_code == 400
    assert 'error' in response.get_json()


# 7. Test update gratitude entry
def test_update_gratitude_entry(client, auth_header):
    post_resp = client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'Old text'})
    entry_id = post_resp.get_json()['entry_id']
    response = client.put(f'/api/child/gratitude/{entry_id}', headers=auth_header, json={'gratitude_text': 'Updated text'})
    assert response.status_code == 200
    assert response.get_json()['gratitude_text'] == 'Updated text'


# 8. Test update fails with blank text
def test_update_gratitude_entry_empty_text(client, auth_header):
    post_resp = client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'Valid text'})
    entry_id = post_resp.get_json()['entry_id']
    response = client.put(f'/api/child/gratitude/{entry_id}', headers=auth_header, json={'gratitude_text': ''})
    assert response.status_code == 400
    assert 'error' in response.get_json()


# 9. Test delete gratitude entry
def test_delete_gratitude_entry(client, auth_header):
    post_resp = client.post('/api/child/gratitude', headers=auth_header, json={'gratitude_text': 'To be deleted'})
    entry_id = post_resp.get_json()['entry_id']
    delete_resp = client.delete(f'/api/child/gratitude/{entry_id}', headers=auth_header)
    assert delete_resp.status_code == 200
    assert 'deleted_entry' in delete_resp.get_json()


# 10. Test delete non-existing entry
def test_delete_nonexistent_gratitude_entry(client, auth_header):
    response = client.delete('/api/child/gratitude/9999', headers=auth_header)
    assert response.status_code == 404
    assert 'error' in response.get_json()


# 11. Test access with no token
def test_create_gratitude_no_auth(client):
    response = client.post('/api/child/gratitude', json={'gratitude_text': 'No token'})
    assert response.status_code == 401


# 12. One child cannot update another child’s entry
def test_child_cannot_update_others_entry(client, auth_header, create_test_child):
    user2, _ = create_test_child()
    access_token2 = create_access_token(identity=str(user2.user_id))
    headers2 = {'Authorization': f'Bearer {access_token2}'}

    post_resp = client.post('/api/child/gratitude', headers=headers2, json={'gratitude_text': 'Private Entry'})
    entry_id = post_resp.get_json()['entry_id']

    update_resp = client.put(f'/api/child/gratitude/{entry_id}', headers=auth_header, json={'gratitude_text': 'Hacked!'})
    assert update_resp.status_code in [403, 404]


# 13. One child cannot delete another child’s entry
def test_child_cannot_delete_others_entry(client, auth_header, create_test_child):
    user2, _ = create_test_child()
    access_token2 = create_access_token(identity=str(user2.user_id))
    headers2 = {'Authorization': f'Bearer {access_token2}'}

    post_resp = client.post('/api/child/gratitude', headers=headers2, json={'gratitude_text': 'Private Entry'})
    entry_id = post_resp.get_json()['entry_id']

    delete_resp = client.delete(f'/api/child/gratitude/{entry_id}', headers=auth_header)
    assert delete_resp.status_code in [403, 404]