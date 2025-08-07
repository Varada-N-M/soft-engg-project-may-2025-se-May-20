# test_password_routes.py
import json
from unittest.mock import MagicMock, patch

import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from models import *


class TestChangePassword:
    """Test cases for /change-password endpoint"""
    
    def test_change_password_success(self, client, create_test_user, app):
        """Test successful password change"""
        user = create_test_user(email="test@example.com")
        
        with app.app_context():
            access_token = create_access_token(identity=str(user.user_id))
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = client.post('api/auth/change-password',
                                 json={
                                     'old_password': 'TestPass123!',
                                     'new_password': 'NewPassword123!'
                                 },
                                 headers=headers)
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Password changed successfully'
            
            # Verify password was actually changed
            updated_user = Users.query.filter_by(user_id=user.user_id).first()
            assert check_password_hash(updated_user.password, 'NewPassword123!')
    
    def test_change_password_wrong_old_password(self, client, create_test_user, app):
        """Test change password with incorrect old password"""
        user = create_test_user(email="test@example.com")
        
        with app.app_context():
            access_token = create_access_token(identity=str(user.user_id))
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = client.post('api/auth/change-password',
                                 json={
                                     'old_password': 'WrongPassword!',
                                     'new_password': 'NewPassword123!'
                                 },
                                 headers=headers)
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['message'] == 'Invalid current password'
    
    def test_change_password_missing_fields(self, client, create_test_user, app):
        """Test change password with missing required fields"""
        user = create_test_user(email="test@example.com")
        
        with app.app_context():
            access_token = create_access_token(identity=str(user.user_id))
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = client.post('/change-password',
                                 json={'old_password': 'TestPass123!'},
                                 headers=headers)
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['error'] == 'Old and new passwords are required'
    
    def test_change_password_unauthorized(self, client):
        """Test change password without authentication"""
        response = client.post('api/auth/change-password',
                             json={
                                 'old_password': 'TestPass123!',
                                 'new_password': 'NewPassword123!'
                             })
        
        assert response.status_code == 401  # JWT will return 401 for missing token
    
    def test_change_password_user_not_found(self, client, app):
        """Test change password for non-existent user"""
        with app.app_context():
            access_token = create_access_token(identity="999999")  # Non-existent user_id
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = client.post('api/auth/change-password',
                                 json={
                                     'old_password': 'TestPass123!',
                                     'new_password': 'NewPassword123!'
                                 },
                                 headers=headers)
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['message'] == 'Invalid current password'