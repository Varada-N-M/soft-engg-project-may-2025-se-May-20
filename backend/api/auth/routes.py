from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                get_jwt_identity, jwt_required)
from datetime import datetime
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from models import *
from utils import *
from werkzeug.security import check_password_hash
from .reset import send_reset_email, confirm_reset_token
from models import Users


class SignupAdmin(Resource):
    def post(self):
        try:
            first_user = Users.query.first()
            if first_user:
                return {'error': 'Admin already exists!'}, 409
            
            data = request.get_json()
            # Required fields for admin
            required_fields = ['email', 'password', 'first_name', 'last_name']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data['last_name'].strip()

            # Validate email and password
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400
            is_valid_password, msg = validate_password(password)
            if not is_valid_password:
                return {'error': msg}, 400

            if Users.query.filter_by(email=email).first():
                return {'error': 'User with this email already exists'}, 409

            hashed_password = generate_password_hash(password)
            new_user = Users(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role_type=UserRole.ADMIN
            )
            db.session.add(new_user)
            db.session.commit()

            # Tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            return {
                'message': 'Admin registered successfully',
                'user_email': new_user.email,
                'role': new_user.role_type.value,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
        

class SignupChild(Resource):
    def post(self):
        try:
            data = request.get_json()

            # Required fields for child
            user_fields = ['email', 'password', 'first_name', 'last_name', 'dob', 'class', 'school_name', 'gender']
            for field in user_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data['last_name'].strip()

            # Validate email and password
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400
            is_valid_password, msg = validate_password(password)
            if not is_valid_password:
                return {'error': msg}, 400

            if Users.query.filter_by(email=email).first():
                return {'error': 'User with this email already exists'}, 409

            hashed_password = generate_password_hash(password)
            new_user = Users(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role_type=UserRole.CHILD
            )
            db.session.add(new_user)
            db.session.flush()  # Get user_id

            # Create Child
            new_child = Child(
                user_id=new_user.user_id,
                dob=datetime.strptime(data['dob'], "%Y-%m-%d").date(),
                class_=data['class'],
                school_name=data['school_name'],
                gender=data['gender'],
                unique_key=generate_unique_key(Child)
            )
            db.session.add(new_child)
            db.session.commit()

            # Tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            return {
                'message': 'Child registered successfully',
                'user_email': new_user.email,
                'role': new_user.role_type.value,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class SignupParent(Resource):
    def post(self):
        try:
            data = request.get_json()

            # Required fields for Users
            user_fields = ['email', 'password', 'first_name', 'last_name', 'phone_number']
            for field in user_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data['last_name'].strip()
            phone_number = data['phone_number']

            # Email and password validation
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400

            is_valid_password, msg = validate_password(password)
            if not is_valid_password:
                return {'error': msg}, 400

            # Check for existing user
            if Users.query.filter_by(email=email).first():
                return {'error': 'User with this email already exists'}, 409

            # Create user
            hashed_password = generate_password_hash(password)
            new_user = Users(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role_type= UserRole.PARENT
            )
            db.session.add(new_user)
            db.session.flush()

            # Create parent profile
            new_parent = Parent(
                user_id=new_user.user_id,
                phone_number=phone_number
            )
            db.session.add(new_parent)
            db.session.commit()

            # Create tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            return {
                'message': 'Parent registered successfully',
                'user_email': new_user.email,
                'role': new_user.role_type.value,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class SignupOrganization(Resource):
    """
    This endpoint allows new users to register an organization.
    It validates the email format and password strength before creating a new user.
    returns a JWT access token and refresh token upon successful registration.
    """
    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['email', 'password', 'first_name', 'last_name', 'organization_name', 'phone_number', 'address']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data['last_name'].strip()
            organization_name = data['organization_name'].strip()
            phone_number = data['phone_number']
            address = data['address']
            
            # Validate email format
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400
            
            # Validate password strength
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                return {'error': password_message}, 400

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
                role_type=UserRole.ORGANIZATION,
            )
            db.session.add(new_user)
            db.session.flush()

            # Create organization
            new_organization = Organization(
                name=organization_name,
                phone_number=phone_number,
                address=address,
                created_by=new_user.user_id
            )
            db.session.add(new_organization)
            db.session.commit()

            # Create access and refresh tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            return {
                'message': 'Organization registered successfully',
                'user_email': new_user.email,
                'role': new_user.role_type.value,
                'organization': new_organization.name,
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
    It validates that the user is logging in from the correct page (parent/child) by cross-checking
    the frontend-provided user type with the actual user type stored in the database.
    Returns a JWT access token and refresh token upon successful login.
    """
    def post(self):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('email') or not data.get('password'):
                return {'error': 'Email and password are required'}, 400
            if not data.get('role_type'):
                return {'error': 'Role type is required'}, 400
            
            email = data['email'].lower().strip()
            password = data['password']
            user_type = data['role_type'].lower().strip()
            
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

            # Check user role type ['admin', 'teacher', 'parent', 'child', 'organization', 'principal']
            if user.role_type.value.lower() != user_type:
                return {'error': 'User role does not match  '}, 403
            
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


class SignupTeacher(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            # Check if this is a principal registration (has school creation data)
            is_principal_registration = data.get('role') == 'principal' or (
                data.get('school_name') and not data.get('school_id')
            )

            # Required fields for teacher/principal
            required_fields = ['email', 'password', 'first_name', 'last_name', 'subject']
            
            # For normal teachers, school_id is required
            # For principals, school creation data is required
            if is_principal_registration:
                required_fields.extend(['school_name'])
            else:
                required_fields.extend(['school_id'])
                
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            email = data['email'].lower().strip()
            password = data['password']
            first_name = data['first_name'].strip()
            last_name = data['last_name'].strip()
            subject = data['subject']

            # Validate email and password
            if not validate_email(email):
                return {'error': 'Invalid email format'}, 400
            is_valid_password, msg = validate_password(password)
            if not is_valid_password:
                return {'error': msg}, 400

            if Users.query.filter_by(email=email).first():
                return {'error': 'User with this email already exists'}, 409

            # Determine role - override automatic assignment if explicitly set
            role = UserRole.PRINCIPAL if is_principal_registration else UserRole.TEACHER
            
            # Create user first
            hashed_password = generate_password_hash(password)
            new_user = Users(
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role_type=role
            )
            db.session.add(new_user)
            db.session.flush()  # Get user_id

            # For principals, create school after user creation
            if is_principal_registration:
                school_name = data['school_name'].strip()
                school_address = data.get('school_address', 'To be provided').strip()
                school_phone = data.get('school_phone', 'To be provided').strip()
                
                # Create the school with the user_id
                new_school = School(
                    name=school_name,
                    address=school_address,
                    phone_number=school_phone,
                    created_by=new_user.user_id
                )
                db.session.add(new_school)
                db.session.flush()  # Get school_id
                school_id = new_school.school_id
            else:
                # For teachers, validate existing school
                school_id = data['school_id']
                if not School.query.get(school_id):
                    return {'error': 'School not found'}, 404

            # Create Teacher record
            new_teacher = Teacher(
                user_id=new_user.user_id,
                subject=subject,
                school_id=school_id
            )
            db.session.add(new_teacher)
            db.session.commit()

            # Tokens
            access_token = create_access_token(identity=str(new_user.user_id))
            refresh_token = create_refresh_token(identity=str(new_user.user_id))

            account_type = 'Principal' if role == UserRole.PRINCIPAL else 'Teacher'
            return {
                'message': f'{account_type} registered successfully',
                'user_email': new_user.email,
                'role': new_user.role_type.value,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'school_id': school_id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ForgotPassword(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email', '').strip().lower()
            if not email:
                return {'error': 'Email is required'}, 400
            user = Users.query.filter_by(email=email).first()
            if user:
                send_reset_email(user)
                return {'message': 'If the email exists, a reset link has been sent.'}, 200
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ResetPassword(Resource):
    def post(self):
        try:
            data = request.get_json()
            token = request.args.get('token')
            new_password = data.get('new_password')

            if not token or not new_password:
                return {'error': 'Token and new password are required'}, 400

            email = confirm_reset_token(token)
            if not email:
                return {'error': 'Invalid or expired token'}, 400

            user = Users.query.filter_by(email=email).first()
            if not user:
                return {'error': 'User not found'}, 404

            user.password = generate_password_hash(new_password)
            db.session.commit()

            return {'message': 'Password reset successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not old_password or not new_password:
                return {'error': 'Old and new passwords are required'}, 400
            
            user = Users.query.filter_by(user_id=current_user_id).first()
            if not user or not check_password_hash(user.password, old_password):
                return {"message": "Invalid current password"}, 400
            
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return {"message": "Password changed successfully"}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
