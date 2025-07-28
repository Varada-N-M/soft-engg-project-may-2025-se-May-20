import json
import uuid
from datetime import date

import pytest
from flask_jwt_extended import create_refresh_token
from werkzeug.security import generate_password_hash

from api.auth.routes import Login
from main import create_app, db
from models import Child, UserRole, Users

from datetime import datetime, timezone


def test_login_success(client, create_test_user):
    """Test successful login with valid credentials"""
    user = create_test_user()
    login_payload = {
        "email": user.email,
        "password": "TestPass123!"
    }
    
    response = client.post('api/login', 
                          json=login_payload,
                          content_type='application/json')
    
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.get_data(as_text=True)}")
    if response.get_json():
        print(f"Response JSON: {response.get_json()}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    # Verify response contains expected data
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'message' in data
    assert 'user' in data
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['message'] == 'Login successful'
    assert data['user'] == user.email


def test_login_missing_email(client):
    """Test login with missing email field"""
    payload = {
        "password": "TestPass123!"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')
    
    print(f"Missing email test - Status: {response.status_code}")
    print(f"Missing email test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'error' in data
    assert data['error'] == 'Email and password are required'


def test_login_missing_password(client):
    """Test login with missing password field"""
    payload = {
        "email": "test@example.com"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Missing password test - Status: {response.status_code}")
    print(f"Missing password test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'error' in data
    assert data['error'] == 'Email and password are required'


def test_login_empty_fields(client):
    """Test login with empty email and password fields"""
    payload = {
        "email": "",
        "password": ""
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Empty fields test - Status: {response.status_code}")
    print(f"Empty fields test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_login_invalid_email(client):
    """Test login with non-existent email"""
    unique_email = f"nonexistent_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "TestPass123!"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Invalid email test - Status: {response.status_code}")
    print(f"Invalid email test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'error' in data
    assert data['error'] == 'Invalid email or password'


def test_login_invalid_password(client, create_test_user):
    """Test login with wrong password"""
    user = create_test_user()
    payload = {
        "email": user.email,
        "password": "WrongPassword123!"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Invalid password test - Status: {response.status_code}")
    print(f"Invalid password test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'error' in data
    assert data['error'] == 'Invalid email or password'



def test_login_case_insensitive_email(client, create_test_user):
    """Test login with different email case"""
    user = create_test_user()
    payload = {
        "email": user.email.upper(),  # Convert to uppercase
        "password": "TestPass123!"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Case insensitive test - Status: {response.status_code}")
    print(f"Case insensitive test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert data['message'] == 'Login successful'


def test_login_email_with_whitespace(client, create_test_user):
    """Test login with email containing whitespace"""
    user = create_test_user()
    payload = {
        "email": f"  {user.email}  ",  # Add whitespace
        "password": "TestPass123!"
    }
    
    response = client.post('api/login', 
                          json=payload,
                          content_type='application/json')

    print(f"Whitespace email test - Status: {response.status_code}")
    print(f"Whitespace email test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert data['message'] == 'Login successful'


def test_login_no_json_data(client):
    """Test login with empty JSON data"""
    response = client.post('api/login', 
                          json={},
                          content_type='application/json')

    print(f"No JSON data test - Status: {response.status_code}")
    print(f"No JSON data test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_login_no_content_type(client, create_test_user):
    """Test login without proper content type"""
    user = create_test_user()
    login_payload = {
        "email": user.email,
        "password": "TestPass123!"
    }
    
    # Send without content_type='application/json'
    response = client.post('api/login', json=login_payload)
    
    print(f"No content type test - Status: {response.status_code}")
    print(f"No content type test - Data: {response.get_data(as_text=True)}")
    
    # Should still work as Flask handles JSON automatically
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_refresh_token_success(client, create_test_user, app):
    """Test successful token refresh"""
    # First login to get refresh token
    user = create_test_user()
    login_payload = {
        "email": user.email,
        "password": "TestPass123!"
    }
    
    login_response = client.post('api/login', 
                                json=login_payload,
                                content_type='application/json')

    assert login_response.status_code == 200
    login_data = login_response.get_json()
    refresh_token = login_data['refresh_token']
    
    # Use refresh token to get new access token
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = client.post('/api/refresh-token', 
                          headers=headers,
                          content_type='application/json')

    print(f"Refresh success test - Status: {response.status_code}")
    print(f"Refresh success test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    data = response.get_json()
    assert data is not None, "Response should contain JSON data"
    assert 'access_token' in data


def test_refresh_token_missing_token(client):
    """Test token refresh without providing a token"""
    response = client.post('api/refresh-token', 
                          content_type='application/json')

    print(f"Missing refresh token test - Status: {response.status_code}")
    print(f"Missing refresh token test - Data: {response.get_data(as_text=True)}")
    
    # JWT will return 401 for missing token
    assert response.status_code == 401, f"Expected 401, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_refresh_token_invalid_token(client):
    """Test token refresh with invalid token"""
    headers = {'Authorization': 'Bearer invalid_token_here'}
    response = client.post('/api/refresh-token', 
                          headers=headers,
                          content_type='application/json')

    print(f"Invalid refresh token test - Status: {response.status_code}")
    print(f"Invalid refresh token test - Data: {response.get_data(as_text=True)}")
    
    # JWT will return 422 for invalid token format
    assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_refresh_token_with_access_token(client, create_test_user):
    """Test token refresh using access token instead of refresh token"""
    # First login to get access token
    user = create_test_user()
    login_payload = {
        "email": user.email,
        "password": "TestPass123!"
    }
    
    login_response = client.post('api/login', 
                                json=login_payload,
                                content_type='application/json')

    assert login_response.status_code == 200
    login_data = login_response.get_json()
    access_token = login_data['access_token']
    
    # Try to use access token for refresh (should fail)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/refresh-token', 
                          headers=headers,
                          content_type='application/json')

    print(f"Access token for refresh test - Status: {response.status_code}")
    print(f"Access token for refresh test - Data: {response.get_data(as_text=True)}")
    
    # Should fail because access token is not a refresh token
    assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}. Response: {response.get_data(as_text=True)}"

