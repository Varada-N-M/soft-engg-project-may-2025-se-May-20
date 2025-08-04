# test_habits.py
import json
from datetime import date, datetime, timezone
from models import Habit, HabitCompletion


class TestHabits:
    """Test cases for Habits resource"""
    
    def test_post_habit_success(self, client, child_user, auth_header, db):
        """Test creating a new habit successfully"""
        user, child = child_user
        
        payload = {
            'habit_name': 'Read for 30 minutes',
            'habit_description': 'Daily reading habit to improve knowledge',
            'habit_category': 'Education',
            'habit_xp': 25
        }
        
        response = client.post(
            '/api/child/habit',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_header
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Habit created successfully'
        assert 'habit_id' in data
        assert 'created_at' in data
        assert data['habit_name'] == payload['habit_name']
        
        # Verify habit was created in database
        habit = Habit.query.filter_by(child_id=child.child_id).first()
        assert habit is not None
        assert habit.name == payload['habit_name']
        assert habit.description == payload['habit_description']
        assert habit.category == payload['habit_category']
        assert habit.habit_xp == payload['habit_xp']
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_post_habit_default_xp(self, client, child_user, auth_header, db):
        """Test creating habit with default XP when not provided"""
        user, child = child_user
        
        payload = {
            'habit_name': 'Exercise daily',
            'habit_description': 'Daily exercise routine',
            'habit_category': 'Health'
        }
        
        response = client.post(
            '/api/child/habit',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_header
        )
        
        assert response.status_code == 201
        
        # Verify default XP was set
        habit = Habit.query.filter_by(child_id=child.child_id).first()
        assert habit.habit_xp == 20  # Default XP
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_post_habit_missing_fields(self, client, auth_header):
        """Test creating habit with missing required fields fails"""
        payload = {
            'habit_name': 'Test habit'
            # Missing description and category
        }
        
        response = client.post(
            '/api/child/habit',
            data=json.dumps(payload),
            content_type='application/json',
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Habit name is required'
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_get_habits_empty(self, client, auth_header):
        """Test getting habits when none exist"""
        response = client.get('/api/child/habit', headers=auth_header)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'No habits found for this child'
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_get_habits_with_data(self, client, child_user, auth_header, db):
        """Test getting habits with created habits and completions"""
        user, child = child_user
        
        # Create test habits
        habit1 = Habit(
            child_id=child.child_id,
            name='Morning exercise',
            description='30 minutes of exercise',
            category='Health',
            habit_xp=20,
            created_at=datetime.now(timezone.utc)
        )
        habit2 = Habit(
            child_id=child.child_id,
            name='Read before bed',
            description='Read for 20 minutes',
            category='Education',
            habit_xp=15,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(habit1)
        db.session.add(habit2)
        db.session.commit()
        
        # Create habit completion
        completion = HabitCompletion(
            child_id=child.child_id,
            habit_id=habit1.id,
            is_done=True,
            completion_date=date.today()
        )
        db.session.add(completion)
        db.session.commit()

        response = client.get('/api/child/habit', headers=auth_header)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'habits_created' in data
        assert 'completed_habits' in data
        assert len(data['habits_created']) == 2
        assert len(data['completed_habits']) == 1
        
        # Verify habit data
        habit_names = [h['name'] for h in data['habits_created']]
        assert 'Morning exercise' in habit_names
        assert 'Read before bed' in habit_names
        
        # Verify completion data
        assert data['completed_habits'][0]['habit_id'] == habit1.id
        assert data['completed_habits'][0]['is_done'] is True
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_put_habit_success(self, client, child_user, auth_header, db):
        """Test updating a habit successfully"""
        user, child = child_user
        
        # Create test habit
        habit = Habit(
            child_id=child.child_id,
            name='Original habit',
            description='Original description',
            category='Original category',
            habit_xp=20,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(habit)
        db.session.commit()
        
        # Update the habit
        update_payload = {
            'habit_name': 'Updated habit name',
            'habit_description': 'Updated description',
            'habit_category': 'Updated category',
            'habit_xp': 30
        }
        
        response = client.put(
            f'/api/child/habit/{habit.id}',
            data=json.dumps(update_payload),
            content_type='application/json',
            headers=auth_header
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Habit updated successfully'
        assert data['habit_name'] == update_payload['habit_name']
        
        # Verify update in database
        updated_habit = Habit.query.get(habit.id)
        assert updated_habit.name == update_payload['habit_name']
        assert updated_habit.description == update_payload['habit_description']
        assert updated_habit.category == update_payload['habit_category']
        assert updated_habit.habit_xp == update_payload['habit_xp']
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_put_habit_not_found(self, client, auth_header):
        """Test updating non-existent habit fails"""
        update_payload = {
            'habit_name': 'Updated name',
            'habit_description': 'Updated description',
            'habit_category': 'Updated category'
        }
        
        response = client.put(
            '/api/child/habit/99999',
            data=json.dumps(update_payload),
            content_type='application/json',
            headers=auth_header
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Habit not found or access denied'
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_delete_habit_success(self, client, child_user, auth_header, db):
        """Test deleting a habit successfully"""
        user, child = child_user
        
        # Create test habit
        habit = Habit(
            child_id=child.child_id,
            name='Habit to delete',
            description='This habit will be deleted',
            category='Test',
            habit_xp=20,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(habit)
        db.session.commit()
        habit_id = habit.id

        response = client.delete(f'/api/child/habit/{habit_id}', headers=auth_header)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Habit deleted successfully'
        assert 'deleted_habit' in data
        
        # Verify deletion in database
        deleted_habit = Habit.query.get(habit_id)
        assert deleted_habit is None
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_delete_habit_not_found(self, client, auth_header):
        """Test deleting non-existent habit fails"""
        response = client.delete('/api/child/habit/99999', headers=auth_header)

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Habit not found or access denied'

        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
class TestCompleteHabit:
    """Test cases for CompleteHabit resource"""
    
    def test_complete_habit_success(self, client, child_user, auth_header, db):
        """Test marking a habit as complete successfully"""
        user, child = child_user
        
        # Create test habit
        habit = Habit(
            child_id=child.child_id,
            name='Daily reading',
            description='Read for 30 minutes',
            category='Education',
            habit_xp=20,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(habit)
        db.session.commit()
        
        response = client.post(
            f'/api/child/habit/{habit.id}/complete',
            headers=auth_header
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Habit done successfully'
        
        # Verify completion was created in database
        completion = HabitCompletion.query.filter_by(
            child_id=child.child_id,
            habit_id=habit.id
        ).first()
        assert completion is not None
        assert completion.is_done is True
        assert completion.completion_date == date.today()
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_complete_habit_already_completed_today(self, client, child_user, auth_header, db):
        """Test marking habit as complete when already completed today fails"""
        user, child = child_user
        
        # Create test habit
        habit = Habit(
            child_id=child.child_id,
            name='Daily reading',
            description='Read for 30 minutes',
            category='Education',
            habit_xp=20,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(habit)
        db.session.commit()
        
        # Create existing completion for today
        existing_completion = HabitCompletion(
            child_id=child.child_id,
            habit_id=habit.id,
            is_done=True,
            completion_date=date.today()
        )
        db.session.add(existing_completion)
        db.session.commit()
        
        response = client.post(
            f'api/child/habit/{habit.id}/complete',
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Habit already completed today'
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_complete_habit_not_found(self, client, auth_header):
        """Test completing non-existent habit fails"""
        response = client.post('api/child/habit/99999/complete', headers=auth_header)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'Habit not found or access denied'
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    
    def test_complete_habit_no_auth(self, client):
        """Test completing habit without authentication fails"""
        response = client.post('api/child/habit/1/complete')
        
        assert response.status_code == 401
        print(f"Response Data: {response.get_data(as_text=True)}")
        if response.get_json():
            print(f"Response JSON: {response.get_json()}")
    