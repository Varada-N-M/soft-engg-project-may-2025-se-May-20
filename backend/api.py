from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re
from models import *


jwt = JWTManager()

# Utility functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"


# JWT Error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': 'Authorization token is required'}), 401


class Signup(Resource):
    """
    User registration endpoint
    This endpoint allows users to register by providing their email, password, and name.
    It validates the email format and password strength before creating a new user.
    returns a JWT access token and refresh token upon successful registration.
    """
    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['email', 'password', 'first_name', 'role_type']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data.get('last_name', '').strip()
            role_type = data['role_type'].lower()
            
            # Validate email format
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400
            
            # Validate password strength
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                return {'error': password_message}, 400

            # Validate role type
            valid_roles = ['teacher', 'parent', 'child', 'admin']
            if role_type not in valid_roles:
                return {'error': f'Role must be one of: {", ".join(valid_roles)}'}, 400
            
            # Check if user already exists
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return {'error': f'User with this email already exists'}, 409
            
            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = Users(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role_type=role_type,
            )
            
            db.session.add(new_user)
            db.session.commit()

            # Create access and refresh tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            return {
                'message': 'User created successfully',
                'user': new_user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201 
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class Login(Resource):
    """
    User login endpoint
    This endpoint allows users to log in by providing their email and password.
    It validates the credentials and returns a JWT access token and refresh token upon successful login.
    """
    def post(self):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('email') or not data.get('password'):
                return {'error': 'Email and password are required'}, 400
            
            email = data['email'].lower().strip()
            password = data['password']
            
            # Find user by email
            user = Users.query.filter_by(email=email).first()
            
            if not user:
                return {'error': 'Invalid email or password'}, 401
            
            # Check if user is active
            if not user.is_active:
                return {'error': 'Account is deactivated. Please contact administrator'}, 401
            
            # Verify password
            if not check_password_hash(user.password, password):
                return {'error': 'Invalid email or password'}, 401
            
            # Create access and refresh tokens
            access_token = create_access_token(identity=str(user.user_id))
            refresh_token = create_refresh_token(identity=str(user.user_id))
            
            return {
                'message': 'Login successful',
                'user': user.email,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
        

class RefreshToken(Resource):
    """
    Refresh token endpoint
    This endpoint allows users to refresh their access token using a valid refresh token.
    """
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user_id = get_jwt_identity()

            # Verify user still exists and is active
            user = Users.query.filter_by(user_id=current_user_id, is_active=True).first()
            if not user:
                return {'error': 'User not found or deactivated'}, 404
            
            # Create new access token
            new_access_token = create_access_token(identity=current_user_id)

            return {'access_token': new_access_token}, 200
        
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
