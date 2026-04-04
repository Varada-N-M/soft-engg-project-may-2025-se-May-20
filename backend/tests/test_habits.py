import json
import uuid
from datetime import date

import pytest
from flask_jwt_extended import create_refresh_token, create_access_token
from werkzeug.security import generate_password_hash

from api.auth.routes import Login
from backend.app import create_app, db
from models import Child, UserRole, Users, Habit

from datetime import datetime, timezone


import pytest
from flask_jwt_extended import create_access_token
from datetime import datetime

def test_create_habit(client, auth_header):
    payload = {'habit_name': 'Read a book',
        'habit_description': 'Read 20 pages',
        'habit_category': 'Learning',
        'habit_xp': 15}

    response = client.post('/api/child/habit', json=payload, headers=auth_header,content_type='application/json')
    
    print(f"Response Status: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 201
    data = response.get_json()
    assert 'habit_id' in data
    assert data['habit_name'] == payload['habit_name']

def test_get_habits(client, auth_header):

    payload = {
        'habit_name': 'Read a book',
        'habit_description': 'Read 20 pages',
        'habit_category': 'Learning',
        'habit_xp': 15
    }

    client.post('/api/child/habit', json=payload, headers=auth_header,content_type='application/json')
    
    response = client.get('/api/child/habit', headers=auth_header)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    data = response.get_json()
    assert 'habits_created' in data
    assert 'completed_habits' in data

def test_update_habit(client, auth_header, child_user):
    _, child = child_user
    habit = Habit(
        child_id=child.child_id,
        name='Old Habit',
        description='Old Desc',
        category='General',
        created_at=datetime.utcnow()
    )
    db.session.add(habit)
    db.session.commit()

    payload = {
        'habit_name': 'New Habit',
        'habit_description': 'New Desc',
        'habit_category': 'Productivity',
        'habit_xp': 30
    }

    response = client.put(f'/api/child/habit/{habit.id}', json=payload, headers=auth_header)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['habit_name'] == 'New Habit'

def test_delete_habit(client, auth_header, child_user):
    _, child = child_user
    habit = Habit(
        child_id=child.child_id,
        name='To Delete',
        description='Desc',
        category='General',
        created_at=datetime.utcnow()
    )
    db.session.add(habit)
    db.session.commit()

    response = client.delete(f'/api/child/habit/{habit.id}', headers=auth_header)
    
    print(f"Response Status: {response.status_code}")
    print(f"Response JSON: {response.get_json()}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Habit deleted successfully'

def test_complete_habit(client, auth_header):
    # Step 1: Create a new habit
    payload = {
        'habit_name': 'Drink water',
        'habit_description': 'Drink 8 glasses of water',
        'habit_category': 'Health',
        'habit_xp': 10
    }
    create_response = client.post('/api/child/habit', json=payload, headers=auth_header)
    assert create_response.status_code == 201
    habit_data = create_response.get_json()
    habit_id = habit_data['habit_id']

    # Step 2: Mark the habit as completed
    complete_response = client.post(f'/api/child/habit/{habit_id}/complete', headers=auth_header)
    
    print(f"Response Status: {complete_response.status_code}")
    print(f"Response JSON: {complete_response.get_json()}")

    assert complete_response.status_code == 200
    assert complete_response.get_json()['message'] == 'Habit done successfully'
