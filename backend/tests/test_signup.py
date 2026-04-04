# test_signup.py 
import json
import uuid
from datetime import date

import pytest

from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from models import Child, Users, UserRole  
from backend.app import db, create_app 


def test_signup_child_success(client, child_payload):
    """Test successful child registration"""
    response = client.post('/api/child/register', 
                          json=child_payload,
                          content_type='application/json')
    
    print(f"Input Payload: {child_payload}")
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.get_data(as_text=True)}")
    if response.get_json():
        print(f"Response JSON: {response.get_json()}")
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    # Verify response contains expected data
    data = response.get_json()
    if data:
        assert 'message' in data or 'user_id' in data or 'success' in data
    

def test_signup_parent_success(client, parent_payload):
    """Test successful parent registration"""
    response = client.post('/api/parent/register', 
                          json=parent_payload,
                          content_type='application/json')
    
    print(f"Input Payload: {parent_payload}")
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_signup_organization_success(client, organization_payload):
    """Test successful organization registration"""
    response = client.post('/api/organization/register', 
                          json=organization_payload,
                          content_type='application/json')
    
    print(f"Input Payload: {organization_payload}")
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_signup_duplicate_email(client, db):
    """Test duplicate email registration with unique email per test"""
    # Generate unique email for this test to avoid conflicts
    unique_email = f"parent_duplicate_{uuid.uuid4().hex[:8]}@example.com"
    
    parent_payload = {
        "email": unique_email,
        "password": "ParentPass123!",
        "first_name": "Jane",
        "last_name": "Doe",
        "phone_number": "9876543210"
    }
    
    # First registration should succeed
    first_response = client.post('/api/parent/register', 
                                json=parent_payload,
                                content_type='application/json')
    
    print(f"First registration - Status: {first_response.status_code}")
    print(f"First registration - Data: {first_response.get_data(as_text=True)}")
    
    # Assert first registration succeeds
    assert first_response.status_code == 201, f"First registration failed with {first_response.status_code}. Response: {first_response.get_data(as_text=True)}"
    
    # Second registration with same email should fail with 409
    second_response = client.post('/api/parent/register', 
                                 json=parent_payload,
                                 content_type='application/json')
    
    print(f"Second registration - Status: {second_response.status_code}")
    print(f"Second registration - Data: {second_response.get_data(as_text=True)}")
    
    assert second_response.status_code == 409, f"Expected 409 for duplicate email, got {second_response.status_code}. Response: {second_response.get_data(as_text=True)}"


def test_signup_child_missing_field(client):
    """Test child registration with missing required field"""
    # Create payload missing the required 'dob' field
    unique_email = f"child_missing_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "StrongPass123!",
        "first_name": "John",
        "last_name": "Doe",
        # "dob": missing this required field
        "class": "5",
        "school_name": "ABC School",
        "gender": "Male"
    }
    
    response = client.post('/api/child/register', 
                          json=payload,
                          content_type='application/json')
    
    print(f"Missing field test - Status: {response.status_code}")
    print(f"Missing field test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.get_data(as_text=True)}"


def test_signup_invalid_email_format(client):
    """Test registration with invalid email format"""
    unique_id = uuid.uuid4().hex[:8]
    payload = {
        "email": "invalid-email",  # Invalid email format
        "password": "StrongPass123!",
        "first_name": "John",
        "last_name": "Doe",
        "dob": str(date(2010, 5, 17)),
        "class": "5",
        "school_name": "ABC School",
        "gender": "Male"
    }
    
    response = client.post('/api/child/register', 
                          json=payload,
                          content_type='application/json')
    
    print(f"Invalid email test - Status: {response.status_code}")
    print(f"Invalid email test - Data: {response.get_data(as_text=True)}")
    
    # Should return 400 for invalid email format
    assert response.status_code == 400


def test_signup_weak_password(client):
    """Test registration with weak password"""
    unique_email = f"parent_weak_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "123",  # Weak password
        "first_name": "Jane",
        "last_name": "Doe",
        "phone_number": "9876543210"
    }
    
    response = client.post('/api/parent/register', 
                          json=payload,
                          content_type='application/json')
    
    print(f"Weak password test - Status: {response.status_code}")
    print(f"Weak password test - Data: {response.get_data(as_text=True)}")
    
    # Should return 400 for weak password
    assert response.status_code == 400


def test_signup_missing_required_fields(client):
    """Test registration with completely missing data"""
    response = client.post('/api/child/register', 
                          json={},
                          content_type='application/json')
    
    print(f"Empty payload test - Status: {response.status_code}")
    print(f"Empty payload test - Data: {response.get_data(as_text=True)}")
    
    assert response.status_code == 400
    
def test_debug_registration_flow(client, db):
    """Debug test to understand registration behavior"""
    from models import Users

    # Check existing users before test
    existing_users_before = Users.query.all()
    print(f"Users before test: {len(existing_users_before)}")
    for user in existing_users_before:
        print(f"Existing user: {user.email}")
    
    unique_email = f"debug_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "DebugPass123!",
        "first_name": "Debug",
        "last_name": "User",
        "phone_number": "1234567890"
    }
    
    # Check what happens with a simple registration
    response = client.post('/api/parent/register', 
                          json=payload,
                          content_type='application/json')
    
    print(f"Debug registration - Status: {response.status_code}")
    print(f"Debug registration - Headers: {dict(response.headers)}")
    print(f"Debug registration - Data: {response.get_data(as_text=True)}")
    
    # Check users after registration attempt
    existing_users_after = Users.query.all()
    print(f"Users after test: {len(existing_users_after)}")
    for user in existing_users_after:
        print(f"User after: {user.email}, Role: {user.role_type}")
    
    # This test is just for debugging, so we'll be lenient with assertions
    assert response.status_code in [200, 201, 400, 409, 422], f"Unexpected status code: {response.status_code}"