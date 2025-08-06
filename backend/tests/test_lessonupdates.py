import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from backend.main import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_student_lesson_updates_get(client, auth_header):
    # Authenticated child user
    response = client.get('/api/child/lesson-updates', headers=auth_header)
    assert response.status_code in (200, 403)  # 200 if lessons exist, 403 if not allowed

    # Unauthenticated
    response = client.get('/api/child/lesson-updates')
    assert response.status_code in (401, 403)

def test_teacher_lesson_updates_get(client, teacher_auth_header):
    # Authenticated teacher user
    response = client.get('/api/teacher/lesson-updates', headers=teacher_auth_header)
    assert response.status_code in (200, 403)  # 200 if lessons exist, 403 if not allowed

    # Unauthenticated
    response = client.get('/api/teacher/lesson-updates')
    assert response.status_code in (401, 403)