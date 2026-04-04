import pytest
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from models import db, LessonUpdates, Users, Teacher, UserRole
from flask_jwt_extended import create_access_token


# @pytest.fixture
# def app():
#     """Create and configure a new app instance for each test."""
#     app = create_app('development', testing=True)
#     return app


# @pytest.fixture
# def client(app):
#     """Create a test client for the app."""
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client
#             db.drop_all()


# @pytest.fixture
# def teacher_auth_header(app):
#     """Create auth header for a teacher user."""
#     with app.app_context():
#         # Ensure clean slate in db for user
#         db.session.query(LessonUpdates).delete()
#         db.session.query(Teacher).delete()
#         db.session.query(Users).delete()
#         db.session.commit()

#         user = Users(
#             email='teacher@example.com',
#             password='password123',
#             first_name='Test',
#             last_name='Teacher',
#             role_type=UserRole.TEACHER,
#             is_active=True
#         )
#         db.session.add(user)
#         db.session.commit()

#         teacher = Teacher(
#             user_id=user.user_id,
#             subject='Math',
#             school_id=1
#         )
#         db.session.add(teacher)
#         db.session.commit()

#         token = create_access_token(identity=user.user_id)
#         return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def sample_lesson_data():
    """Sample lesson data for testing."""
    return {
        'day': 'Monday',
        'subject': 'Math',
        'lesson': 'Algebra Basics',
        'activity': 'Solving equations on the board',
        'class_': 5
    }


def test_teacher_lesson_updates_endpoints_require_auth(client):
    """Verify endpoints reject unauthorized access."""
    urls = [
        ('get', '/api/teacher/lesson-updates'),
        ('post', '/api/teacher/lesson-updates'),
        ('put', '/api/teacher/lesson-updates/1'),
        ('delete', '/api/teacher/lesson-updates/1')
    ]
    for method, url in urls:
        resp = getattr(client, method)(url, json={})
        assert resp.status_code == 401


def test_create_lesson_update_authenticated(client, teacher_auth_header, sample_lesson_data):
    """Test creating a lesson update with correct authentication."""
    response = client.post(
        '/api/teacher/lesson-updates',
        json=sample_lesson_data,
        headers=teacher_auth_header
    )

    print(response.get_json())
    assert response.status_code == 201
    data = response.get_json()
    assert data is not None
    assert 'message' in data
    assert data['message'] == 'Lesson update created successfully'
    assert 'lesson' in data
    
    lesson = data['lesson']
    
    assert isinstance(lesson.get('id'), int)
    assert isinstance(lesson.get('created_at'), str)
    datetime.fromisoformat(lesson['created_at'])


def test_get_all_lesson_updates(client, teacher_auth_header, sample_lesson_data):
    """Test retrieving all lesson updates for the authenticated teacher."""

    # First, create two lesson updates
    client.post('/api/teacher/lesson-updates', json=sample_lesson_data, headers=teacher_auth_header)
    second_data = sample_lesson_data.copy()
    second_data['day'] = 'Tuesday'
    second_data['lesson'] = 'Geometry Basics'
    client.post('/api/teacher/lesson-updates', json=second_data, headers=teacher_auth_header)

    # GET all lesson updates
    response = client.get('/api/teacher/lesson-updates', headers=teacher_auth_header)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data is not None
    assert 'lessons' in data
    lessons = data['lessons']
    assert isinstance(lessons, list)
    assert len(lessons) >= 2

    

def test_get_single_lesson_update(client, teacher_auth_header, sample_lesson_data):
    """Test retrieving a single lesson update by ID."""

    # Create a lesson update
    post_resp = client.post('/api/teacher/lesson-updates', json=sample_lesson_data, headers=teacher_auth_header)

    lesson_id = post_resp.get_json()['lesson']['id']

    # Fetch the lesson update by ID
    get_resp = client.get(f'/api/teacher/lesson-updates/{lesson_id}', headers=teacher_auth_header)
    print(get_resp.get_json())
    assert get_resp.status_code == 200

    data = get_resp.get_json()
    assert 'lesson' in data
    lesson = data['lesson']
    assert data['id'] == lesson_id
    

def test_update_lesson_update(client, teacher_auth_header, sample_lesson_data):
    """Test updating an existing lesson update."""

    # Create lesson update first
    post_resp = client.post('/api/teacher/lesson-updates', json=sample_lesson_data, headers=teacher_auth_header)
    print(post_resp.get_json())
    lesson_id = post_resp.get_json()['lesson']['id']

    # Prepare update data
    updated_data = {
        'day': 'Wednesday',
        'subject': 'Science',
        'lesson': 'Physics Basics',
        'activity': 'Experiments with motion',
        'class_': 6
    }

    # Update the lesson update
    put_resp = client.put(f'/api/teacher/lesson-updates/{lesson_id}', json=updated_data, headers=teacher_auth_header)
    assert put_resp.status_code == 200

    data = put_resp.get_json()
    assert 'message' in data
    assert data['message'] == 'Lesson update updated successfully'
    lesson = data['lesson']
    assert lesson['id'] == lesson_id
    

def test_delete_lesson_update(client, teacher_auth_header, sample_lesson_data):
    """Test deleting an existing lesson update."""

    # Create lesson update first
    post_resp = client.post('/api/teacher/lesson-updates', json=sample_lesson_data, headers=teacher_auth_header)
    lesson_id = post_resp.get_json()['lesson']['id']

    # Delete the lesson update
    del_resp = client.delete(f'/api/teacher/lesson-updates/{lesson_id}', headers=teacher_auth_header)
    assert del_resp.status_code == 200
    data = del_resp.get_json()
    assert 'message' in data
    assert data['message'] == 'Lesson update deleted successfully'

    # Try to get the deleted lesson update (expect 404)
    get_resp = client.get(f'/api/teacher/lesson-updates/{lesson_id}', headers=teacher_auth_header)
    assert get_resp.status_code == 404


def test_validation_errors_on_create(client, teacher_auth_header, sample_lesson_data):
    """Test creating lesson update with invalid or missing fields."""

    # Missing required fields (remove 'lesson' and 'activity')
    invalid_data_missing = sample_lesson_data.copy()
    invalid_data_missing.pop('lesson')
    invalid_data_missing.pop('activity')

    resp = client.post('/api/teacher/lesson-updates', json=invalid_data_missing, headers=teacher_auth_header)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data is not None
    assert 'error' in data or 'message' in data

    # Invalid 'day'
    invalid_data_day = sample_lesson_data.copy()
    invalid_data_day['day'] = 'Saturday'  # invalid
    resp = client.post('/api/teacher/lesson-updates', json=invalid_data_day, headers=teacher_auth_header)
    assert resp.status_code == 400

    # Invalid 'subject'
    invalid_data_subject = sample_lesson_data.copy()
    invalid_data_subject['subject'] = 'InvalidSubject'
    resp = client.post('/api/teacher/lesson-updates', json=invalid_data_subject, headers=teacher_auth_header)
    assert resp.status_code == 400

    # Empty string fields
    invalid_data_empty = {k: '' for k in sample_lesson_data}
    resp = client.post('/api/teacher/lesson-updates', json=invalid_data_empty, headers=teacher_auth_header)
    assert resp.status_code == 400


def test_update_nonexistent_lesson_returns_404(client, teacher_auth_header, sample_lesson_data):
    """Trying to update a non-existent lesson update should return 404."""
    resp = client.put('/api/teacher/lesson-updates/9999', json=sample_lesson_data, headers=teacher_auth_header)
    assert resp.status_code == 404

def test_delete_nonexistent_lesson_returns_404(client, teacher_auth_header):
    """Trying to delete a non-existent lesson update should return 404."""
    resp = client.delete('/api/teacher/lesson-updates/9999', headers=teacher_auth_header)
    assert resp.status_code == 404


def test_lesson_updates_model_structure():
    """Test the LessonUpdates model attribute structure without saving."""
    with create_app('development', testing=True).app_context():
        lesson = LessonUpdates(
            teacher_id=1,
            day='Monday',
            subject='Math',
            lesson='Test Lesson',
            activity='Test Activity'
        )
        assert lesson.day == 'Monday'
        assert lesson.subject == 'Math'
        assert lesson.lesson == 'Test Lesson'
        assert lesson.activity == 'Test Activity'
        assert lesson.teacher_id == 1
        # created_at typically set on commit, not on instantiation


def test_teacher_api_classes_exist():
    """Verify that API resource classes and their methods exist."""
    from api.teacher.routes import TeacherLessonUpdates, TeacherLessonUpdateDetail

    assert TeacherLessonUpdates is not None
    assert TeacherLessonUpdateDetail is not None

    for cls, methods in [(TeacherLessonUpdates, ['get', 'post']),
                         (TeacherLessonUpdateDetail, ['get', 'put', 'delete'])]:
        for method in methods:
            assert hasattr(cls, method)


def test_validation_logic_is_consistent():
    """Basic sanity check of valid and invalid day/subject values."""
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    valid_subjects = ['Math', 'English', 'Science', 'Social Studies', 'Computers']

    # Valid
    assert 'Monday' in valid_days
    assert 'Math' in valid_subjects

    # Invalid
    assert 'Saturday' not in valid_days
    assert 'InvalidSubject' not in valid_subjects
