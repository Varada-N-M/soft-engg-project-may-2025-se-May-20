import uuid
from datetime import date, datetime, timezone

import pytest
from flask_jwt_extended import create_access_token

from models import (Child, CommonSkill, School, SkillCompleted, Teacher,
                    UserRole, Users)


class TestSkillsAPI:
    """Essential test cases for Skills API endpoints - CRUD operations"""

    def test_get_skills_success_child_user(self, client, db, create_test_child, auth_header):
        """Test GET /api/child/skills - Success for child user with skills"""
        user, child = create_test_child()
        
        # Create some common skills
        skill1 = CommonSkill(
            skill_name="Python Programming",
            video_url="https://example.com/python",
            skill_xp=100
        )
        skill2 = CommonSkill(
            skill_name="Math Basics",
            video_url="https://example.com/math", 
            skill_xp=50
        )
        db.session.add_all([skill1, skill2])
        db.session.flush()
        
        # Mark one skill as completed
        completed_skill = SkillCompleted(
            child_id=child.child_id,
            skill_id=skill1.id,
            is_learned=True,
            completion_date=datetime.now(timezone.utc)
        )
        db.session.add(completed_skill)
        db.session.commit()

        response = client.get('/api/child/skills', headers=auth_header)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'skills' in data
        assert len(data['skills']) == 2
        
        # Verify skills are present (flexible assertion for API variations)
        skill_names = [s['skill_name'] for s in data['skills']]
        assert 'Python Programming' in skill_names
        assert 'Math Basics' in skill_names

    def test_get_skills_no_skills_found(self, client, db, create_test_child, auth_header):
        """Test GET /api/child/skills - No skills in database"""
        user, child = create_test_child()

        response = client.get('/api/child/skills', headers=auth_header)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'No skills found'

    def test_get_skills_unauthorized_non_child(self, client, db, create_test_user):
        """Test GET /api/child/skills - Unauthorized for non-child user"""
        teacher = create_test_user(role=UserRole.TEACHER)
        db.session.commit()
        
        access_token = create_access_token(identity=str(teacher.user_id))
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.get('/api/child/skills', headers=headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'Only active child users can view skills'

    def test_post_skill_success_teacher(self, client, db, teacher_user, teacher_auth_header):
        """Test POST /api/child/skills - Success for teacher creating skill"""
        skill_data = {
            "skill_name": "Advanced Mathematics",
            "video_url": "https://example.com/advanced-math",
            "skill_xp": 150
        }

        response = client.post('/api/child/skills', json=skill_data, headers=teacher_auth_header)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Skill added successfully'
        
        # Verify skill was created in database
        skill = CommonSkill.query.filter_by(skill_name="Advanced Mathematics").first()
        assert skill is not None
        assert skill.video_url == "https://example.com/advanced-math"
        assert skill.skill_xp == 150

    def test_post_skill_unauthorized_child_user(self, client, db, create_test_child, auth_header):
        """Test POST /skills - Unauthorized for child user"""
        skill_data = {
            "skill_name": "Test Skill",
            "video_url": "https://example.com/test",
            "skill_xp": 50
        }

        response = client.post('/api/child/skills', json=skill_data, headers=auth_header)
        
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'Only teachers and principals can add skills'

    def test_post_skill_missing_required_fields(self, client, db, teacher_user, teacher_auth_header):
        """Test POST /skills - Missing required fields"""
        skill_data = {
            "video_url": "https://example.com/test",
            "skill_xp": 50
            # Missing skill_name
        }

        response = client.post('/api/child/skills', json=skill_data, headers=teacher_auth_header)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Skill name and video URL are required'

    def test_put_skill_success(self, client, db, teacher_user, teacher_auth_header):
        """Test PUT /skills/<id> - Success updating skill"""
        # Create a skill to update
        skill = CommonSkill(
            skill_name="Original Skill",
            video_url="https://example.com/original",
            skill_xp=50
        )
        db.session.add(skill)
        db.session.commit()
        
        update_data = {
            "skill_name": "Updated Skill",
            "video_url": "https://example.com/updated",
            "skill_xp": 100
        }

        response = client.put(f'/api/child/skills/{skill.id}', json=update_data, headers=teacher_auth_header)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Skill updated successfully'
        
        # Verify updates in database
        updated_skill = CommonSkill.query.get(skill.id)
        assert updated_skill.skill_name == "Updated Skill"
        assert updated_skill.video_url == "https://example.com/updated"
        assert updated_skill.skill_xp == 100

    def test_put_skill_not_found(self, client, db, teacher_user, teacher_auth_header):
        """Test PUT /skills/<id> - Skill not found"""
        update_data = {
            "skill_name": "Updated Skill",
            "video_url": "https://example.com/updated",
            "skill_xp": 100
        }

        response = client.put('/api/child/skills/999', json=update_data, headers=teacher_auth_header)
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Skill not found'

    def test_delete_skill_success(self, client, db, teacher_user, teacher_auth_header):
        """Test DELETE /skills/<id> - Success deleting skill"""
        skill = CommonSkill(
            skill_name="Skill to Delete",
            video_url="https://example.com/delete",
            skill_xp=50
        )
        db.session.add(skill)
        db.session.commit()
        skill_id = skill.id

        response = client.delete(f'/api/child/skills/{skill_id}', headers=teacher_auth_header)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Skill deleted successfully'
        
        # Verify skill was deleted
        deleted_skill = CommonSkill.query.get(skill_id)
        assert deleted_skill is None
    def test_complete_skill_unauthorized_non_child(self, client, db, create_test_user):
        """Test POST /skills/<id>/complete - Unauthorized for non-child user"""
        teacher = create_test_user(role=UserRole.TEACHER)
        db.session.commit()
        
        skill = CommonSkill(
            skill_name="Test Skill",
            video_url="https://example.com/test",
            skill_xp=50
        )
        db.session.add(skill)
        db.session.commit()
        
        access_token = create_access_token(identity=str(teacher.user_id))
        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.post(f'/api/child/skills/{skill.id}/complete', headers=headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'Only active child users can mark skills as learned'


@pytest.fixture
def common_skills(db):
    """Create multiple common skills for testing"""
    skills = [
        CommonSkill(skill_name="Python Basics", video_url="https://example.com/python", skill_xp=100),
        CommonSkill(skill_name="Math Fundamentals", video_url="https://example.com/math", skill_xp=75),
        CommonSkill(skill_name="Science Concepts", video_url="https://example.com/science", skill_xp=50),
    ]
    db.session.add_all(skills)
    db.session.commit()
    return skills