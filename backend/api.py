from datetime import date, datetime, timedelta, timezone
from sqlalchemy import func
from flask import jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from models import *
from utils import *
from werkzeug.security import check_password_hash, generate_password_hash


jwt = JWTManager()


# --- JWT Error handlers --- #
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': 'Authorization token is required'}), 401


# --- API Endpoints --- # 
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
       
        
class GratitudeEntry(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new gratitude entry for the logged-in child user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can post gratitude entries'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            data = request.get_json()
            gratitude_text = data.get('gratitude_text', '').strip()

            if not gratitude_text:
                return {'error': 'Gratitude text is required'}, 400

            entry = GratitudeEntries(
                child_id=child.child_id,
                gratitude_text=gratitude_text,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(entry)
            db.session.commit()

            return {
                'message': 'Gratitude entry created successfully',
                'entry_id': entry.entry_id,
                'created_at': entry.created_at.isoformat(),
                'gratitude_text': entry.gratitude_text
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def get(self):
        """
        Get gratitude entries for the logged-in child.
        Supports:
        - ?date=DD-MM-YY → entries on that specific day
        - ?days=N        → entries in the past N days
        - No params      → all entries
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can view gratitude entries'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            query = GratitudeEntries.query.filter_by(child_id=child.child_id)

            # Filter by specific date
            date_str = request.args.get('date')
            if date_str:
                try:
                    target_date = datetime.strptime(date_str, "%d-%m-%y").date()

                    # ⛔ Reject future dates
                    if target_date > date.today():
                        return {'error': 'Date cannot be in the future'}, 400

                    query = query.filter(func.date(GratitudeEntries.created_at) == target_date)

                except ValueError:
                    return {'error': 'Invalid date format. Use DD-MM-YY'}, 400

            # Filter by last N days
            days = request.args.get('days')
            if days and not date_str:
                try:
                    days = int(days)
                    from_date = datetime.now(tz=timezone.utc) - timedelta(days=days)
                    query = query.filter(GratitudeEntries.created_at >= from_date)
                except ValueError:
                    return {'error': 'Invalid days value. Must be an integer.'}, 400

            entries = query.order_by(GratitudeEntries.created_at.desc()).all()

            if not entries:
                return {'message': 'No gratitude entries found for the requested date or time period.'}, 200

            return {
                'entries': [
                    {
                        'entry_id': entry.entry_id,
                        'created_at': entry.created_at.isoformat(),
                        'gratitude_text': entry.gratitude_text
                    } for entry in entries
                ]
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def put(self, entry_id):
        """
        Update a specific gratitude entry for the logged-in child user.
        URL: /gratitude/<int:entry_id>
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can update gratitude entries'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the entry and verify ownership
            entry = GratitudeEntries.query.filter_by(
                entry_id=entry_id,
                child_id=child.child_id
            ).first()

            if not entry:
                return {'error': 'Gratitude entry not found or access denied'}, 404

            data = request.get_json()
            gratitude_text = data.get('gratitude_text', '').strip()

            if not gratitude_text:
                return {'error': 'Gratitude text is required'}, 400

            # Update the entry
            entry.gratitude_text = gratitude_text
            entry.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()

            return {
                'message': 'Gratitude entry updated successfully',
                'entry_id': entry.entry_id,
                'created_at': entry.updated_at.isoformat(),
                'gratitude_text': entry.gratitude_text
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def delete(self, entry_id):
        """
        Delete a specific gratitude entry for the logged-in child user.
        URL: /gratitude/<int:entry_id>
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can delete gratitude entries'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the entry and verify ownership
            entry = GratitudeEntries.query.filter_by(
                entry_id=entry_id,
                child_id=child.child_id
            ).first()

            if not entry:
                return {'error': 'Gratitude entry not found or access denied'}, 404

            # Store entry details for response before deletion
            entry_details = {
                'entry_id': entry.entry_id,
                'created_at': entry.created_at.isoformat(),
                'gratitude_text': entry.gratitude_text
            }

            # Delete the entry
            db.session.delete(entry)
            db.session.commit()

            return {
                'message': 'Gratitude entry deleted successfully',
                'deleted_entry': entry_details
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
        
        
        








        
        

