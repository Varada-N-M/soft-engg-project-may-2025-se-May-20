# test_password_routes.py
import json
from unittest.mock import MagicMock, patch

import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from api.auth.reset import generate_reset_token, send_reset_email
from models import Users

class TestResetPassword:
    """Test cases for /reset-password endpoint"""
    
    def test_reset_password_success(self, client, create_test_user):
        """Test successful password reset"""
        user = create_test_user(email="test@example.com")
        
        with patch('api.auth.reset.confirm_reset_token') as mock_confirm:
            mock_confirm.return_value = "test@example.com"

            response = client.post('api/auth/reset-password?token=valid_token',
                                 json={'new_password': 'NewPassword123!'})
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == 'Password reset successfully'
            
            # Verify password was actually changed
            updated_user = Users.query.filter_by(email="test@example.com").first()
            assert check_password_hash(updated_user.password, 'NewPassword123!')
    
    def test_reset_password_with_real_token(self, client, create_test_user):
        """Test password reset with actual token generation"""
        
        
        user = create_test_user(email="test@example.com")
        
        # Generate a real token
        real_token = generate_reset_token(user.email)
        
        response = client.post(f'/reset-password?token={real_token}',
                             json={'new_password': 'NewPassword123!'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Password reset successfully'
        
        # Verify password was actually changed
        updated_user = Users.query.filter_by(email="test@example.com").first()
        assert check_password_hash(updated_user.password, 'NewPassword123!')
    
    def test_reset_password_expired_token(self, client, create_test_user):
        """Test password reset with expired token"""
        import time

        
        
        user = create_test_user(email="test@example.com")
        
        # Create an expired token by mocking time
        with patch('time.time', return_value=time.time() - 7200):  # 2 hours ago
            expired_token = generate_reset_token(user.email)
        
        response = client.post(f'/reset-password?token={expired_token}',
                             json={'new_password': 'NewPassword123!'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid or expired token'
    
    def test_reset_password_invalid_token(self, client):
        """Test reset password with invalid token"""
        with patch(f'confirm_reset_token') as mock_confirm:
            mock_confirm.return_value = None
            
            response = client.post('/reset-password?token=invalid_token',
                                 json={'new_password': 'NewPassword123!'})
            
            assert response.status_code == 400
            data = json.loads(response.data)
            assert data['error'] == 'Invalid or expired token'
    
    def test_reset_password_missing_token(self, client):
        """Test reset password without token"""
        response = client.post('/reset-password',
                             json={'new_password': 'NewPassword123!'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Token and new password are required'
    
    def test_reset_password_missing_new_password(self, client):
        """Test reset password without new password"""
        response = client.post('api/auth/reset-password?token=valid_token', json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Token and new password are required'
    
    def test_reset_password_user_not_found(self, client):
        """Test reset password when user doesn't exist"""
        with patch(f'confirm_reset_token') as mock_confirm:
            mock_confirm.return_value = "nonexistent@example.com"
            
            response = client.post('/reset-password?token=valid_token',
                                 json={'new_password': 'NewPassword123!'})
            
            assert response.status_code == 404
            data = json.loads(response.data)
            assert data['error'] == 'User not found'
