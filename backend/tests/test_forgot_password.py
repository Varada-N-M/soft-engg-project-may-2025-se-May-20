# test_password_routes.py
import json
from unittest.mock import MagicMock, patch

import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from api.auth.reset import generate_reset_token, send_reset_email
from models import Users

  # Import the reset module to access its functions



class TestForgotPassword:
    """Test cases for /forgot-password endpoint"""
    
    def test_forgot_password_success(self, client, create_test_user):
        user = create_test_user(email="test@example.com")

        with patch('api.auth.routes.send_reset_email') as mock_send_email:  # <-- FIXED HERE
            mock_send_email.return_value = "http://frontend.com/reset?token=abc123"

            response = client.post('api/auth/forgot-password', json={'email': 'test@example.com'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'If the email exists' in data['message']
            mock_send_email.assert_called_once_with(user)

    # Test function correction
    def test_forgot_password_nonexistent_email(self, client):
        with patch('api.auth.reset.send_reset_email') as mock_send_email:
            response = client.post('/api/auth/forgot-password', 
                                json={'email': 'nonexistent@example.com'})
            
            assert response.status_code == 200
            response_data = response.get_json()
            assert 'message' in response_data
            assert 'If the email exists' in response_data['message']
            mock_send_email.assert_not_called()


    def test_forgot_password_no_mocking(self, client, create_test_user):
        """Test forgot password without mocking - will actually print reset URL"""
        user = create_test_user(email="test@example.com")

        response = client.post('api/auth/forgot-password',
                             json={'email': 'test@example.com'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'If the email exists' in data['message']
        # This will actually call send_reset_email and print the reset URL
    
    def test_forgot_password_missing_email(self, client):
        """Test forgot password without email"""
        response = client.post('api/auth/forgot-password', json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Email is required'
    
    def test_forgot_password_empty_email(self, client):
        """Test forgot password with empty email"""
        response = client.post('api/auth/forgot-password', json={'email': '  '})

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Email is required'

