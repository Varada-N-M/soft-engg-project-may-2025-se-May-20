# conftest.py - Updated to match actual model structure
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
import uuid

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from main import create_app
from main import db as _db
from models import Child, UserRole, Users


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app(testing=True)
    
    # Set test configuration
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        try:
            _db.create_all()
            yield app
        except Exception as e:
            print(f"Database setup error: {e}")
            raise
        finally:
            _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Return database instance and clean after test"""
    with app.app_context():
        # Clear all tables at the start of each test
        _db.session.remove()
        _db.drop_all()
        _db.create_all()
        
        yield _db
        
        # Clean up after test
        _db.session.remove()


@pytest.fixture(scope='function')
def client(app, db):
    """Return test client"""
    return app.test_client()


@pytest.fixture
def create_test_user(db):
    """Create a test user with correct field names"""
    def _create_user(role=UserRole.CHILD, email="test@example.com", **kwargs):
        try:
            # Build user data with correct field names from Users model
            user_data = {
                'email': email,
                'first_name': 'Test',
                'last_name': 'User',
                'role_type': role,  # Correct field name from model
                'password': generate_password_hash('TestPass123!'),  # Correct field name
                'is_active': True,
                'created_at': datetime.utcnow()
            }
            
            # Add any custom fields
            user_data.update(kwargs)
            
            user = Users(**user_data)
            db.session.add(user)
            db.session.flush()  # Get user_id
            
            return user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            print(f"Available Users fields: {[col.name for col in Users.__table__.columns]}")
            raise
    
    return _create_user


@pytest.fixture
def create_test_child(db, create_test_user):
    """Create a test child with correct field names"""
    def _create_child(email="child@example.com", **kwargs):
        try:
            # Create the user first
            user = create_test_user(role=UserRole.CHILD, email=email)
            
            # Build child data with correct field names from Child model
            child_data = {
                'user_id': user.user_id,
                'dob': date(2010, 5, 15),
                'class_': 5,  # Correct field name from model (class_ maps to 'class' column)
                'school_name': 'Test School',
                'gender': 'Male',
                'is_linked': False,
                'streak': 0,
                'xp_points': 0,
                'created_at': datetime.utcnow()
            }
            
            # Add any custom fields
            child_data.update(kwargs)
            
            child = Child(**child_data)
            db.session.add(child)
            db.session.commit()
            
            return user, child
            
        except Exception as e:
            print(f"Error creating child: {e}")
            print(f"Available Child fields: {[col.name for col in Child.__mapper__.columns]}")
            raise
    
    return _create_child


# Fixtures specifically for gratitude tests
@pytest.fixture
def child_user(create_test_child):
    """Create a child user for gratitude tests"""
    unique_email = f"gratitude_child_{uuid.uuid4().hex[:8]}@example.com"
    return create_test_child(email=unique_email)


@pytest.fixture
def auth_header(child_user):
    """Create authentication header for child user"""
    user, _ = child_user
    access_token = create_access_token(identity=user.user_id)
    return {'Authorization': f'Bearer {access_token}'}


# Sample payloads for registration tests with unique emails and correct field names
@pytest.fixture
def child_payload():
    unique_email = f"child_{uuid.uuid4().hex[:8]}@example.com"
    return {
        "email": unique_email,
        "password": "StrongPass123!",
        "first_name": "John",
        "last_name": "Doe",
        "dob": str(date(2010, 5, 17)),
        "class": "5",  # This will need to be mapped to class_ field in your registration endpoint
        "school_name": "ABC School",
        "gender": "Male"
    }


@pytest.fixture
def parent_payload():
    unique_email = f"parent_{uuid.uuid4().hex[:8]}@example.com"
    return {
        "email": unique_email,
        "password": "ParentPass123!",
        "first_name": "Jane",
        "last_name": "Doe",
        "phone_number": "9876543210"
    }


@pytest.fixture
def organization_payload():
    unique_email = f"org_{uuid.uuid4().hex[:8]}@example.com"
    return {
        "email": unique_email,
        "password": "OrgPass123!",
        "first_name": "Alice",
        "last_name": "Smith",
        "organization_name": "Test Org",
        "phone_number": "1234567890",
        "address": "123 Main Street"
    }