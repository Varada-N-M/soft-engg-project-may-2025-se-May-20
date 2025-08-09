from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime, timedelta, timezone, date
from sqlalchemy import func
from flask_restful import Resource
from models import *
from utils import *


class LinkChildToParent(Resource):
    @jwt_required()
    def post(self):
        """
        Link a child to a parent using the child's unique key.
        """
        try:
            user_id = get_jwt_identity()
            data = request.get_json()

            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'message': 'Parent not found'}, 404

            if not data or 'child_key' not in data:
                return {'message': 'Child key is required'}, 400
            
            child_key = data['child_key']
            child = Child.query.filter_by(unique_key=child_key).first()
            if not child:
                return {'message': 'Child not found'}, 404
            if child.is_linked:
                return {'message': 'Child is already linked to a parent'}, 400
            
            link = ParentChild(
                parent_id=parent.parent_id,
                child_id=child.child_id,
                linked_at=datetime.utcnow()
            )
            db.session.add(link)
            child.is_linked = True  # Update child's linked status
            db.session.commit()
            return {'message': 'Child linked successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred while linking child to parent', 'error': str(e)}, 500
        
    
    @jwt_required()
    def put(self, child_id):
        """
        Unlink a child from a parent.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'message': 'Parent not found'}, 404
            
            link = ParentChild.query.filter_by(parent_id=parent.parent_id, child_id=child_id).first()
            if not link:
                return {'message': 'Link not found'}, 404
            
            db.session.delete(link)
            child = Child.query.get(child_id)
            if child:
                child.is_linked = False  # Update child's linked status
            db.session.commit()
            return {'message': 'Child unlinked successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred while unlinking child from parent', 'error': str(e)}, 500
        
class ParentProfile(Resource):
    @jwt_required()
    def get(self):
        """
        Get the profile of the logged-in parent user.
        Returns basic information about the parent user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.PARENT).first()

            if not user:
                return {'error': 'Only active parent users can view their profile'}, 403

            parent = Parent.query.filter_by(user_id=user.user_id).first()
            if not parent:
                return {'error': 'parent profile not found'}, 404

            profile_data = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': parent.phone_number,
                'parent_id': parent.parent_id
            }
            
            return {'profile': profile_data}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


#### The query used in this need to optimize ####
class GetLinkedChildren(Resource):
    @jwt_required()
    def get(self):
        """
        Get all children linked to the current parent.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'message': 'Parent not found'}, 404
            
            # Use joins to get linked children data
            linked_children_query = (
                db.session.query(
                    Child.child_id,
                    Child.dob,
                    Child.class_,
                    Child.school_name,
                    Child.gender,
                    Child.unique_key,
                    Child.is_linked,
                    Child.created_at,
                    Child.streak,
                    Child.xp_points,
                    Users.first_name,
                    Users.last_name,
                    Users.email,
                    ParentChild.linked_at
                )
                .join(ParentChild, Child.child_id == ParentChild.child_id)
                .join(Users, Child.user_id == Users.user_id)
                .filter(ParentChild.parent_id == parent.parent_id)
                .filter(Child.is_linked == True)
                .order_by(ParentChild.linked_at.desc())
            )
            if not linked_children_query:
                return {'message': 'No linked children found'}, 404

            # Execute the query
            results = linked_children_query.all()
            
            # Format the data
            children_data = []
            for result in results:
                child_data = {
                    'child_id': result.child_id,
                    'first_name': result.first_name,
                    'last_name': result.last_name,
                    'email': result.email,
                    'date_of_birth': result.dob.isoformat() if result.dob else None,
                    'class': result.class_,
                    'school_name': result.school_name,
                    'gender': result.gender,
                    'unique_key': result.unique_key,
                    'is_linked': result.is_linked,
                    'created_at': result.created_at.isoformat(),
                    'linked_at': result.linked_at.isoformat(),
                    'streak': result.streak,
                    'xp_points': result.xp_points
                }
                children_data.append(child_data)
            
            return {
                'linked_children': children_data
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'An error occurred while retrieving linked children', 
                'error': str(e)}, 500


class ParentChildrenLessonUpdates(Resource):
    @jwt_required()
    def get(self):
        """
        Get lesson updates for all children linked to the current parent.
        Returns lesson updates from teachers for all linked children.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'message': 'Parent not found'}, 404
            
            # Get all linked children for this parent
            linked_children_query = (
                db.session.query(Child)
                .join(ParentChild, Child.child_id == ParentChild.child_id)
                .filter(ParentChild.parent_id == parent.parent_id)
                .filter(Child.is_linked == True)
            )
            
            linked_children = linked_children_query.all()
            
            if not linked_children:
                return {'message': 'No linked children found', 'lesson_updates': []}, 200
            
            # Get all lesson updates for the linked children's classes
            class_levels = [child.class_ for child in linked_children if child.class_]
            
            if not class_levels:
                return {'message': 'No class information available for children', 'lesson_updates': []}, 200
            
            # Get lesson updates for these class levels
            lesson_updates_query = (
                db.session.query(LessonUpdates, Teacher, Users)
                .join(Teacher, LessonUpdates.teacher_id == Teacher.teacher_id)
                .join(Users, Teacher.user_id == Users.user_id)
                .filter(LessonUpdates.class_.in_(class_levels))
                .order_by(LessonUpdates.created_at.desc())
                .limit(50)  # Limit to recent updates
            )
            
            lesson_updates = lesson_updates_query.all()
            
            # Format the data
            result = []
            for lesson_update, teacher, teacher_user in lesson_updates:
                # Find which children this lesson applies to
                applicable_children = [
                    child for child in linked_children 
                    if child.class_ == lesson_update.class_
                ]
                
                lesson_data = {
                    'id': lesson_update.id,
                    'teacher_name': f"{teacher_user.first_name} {teacher_user.last_name}",
                    'teacher_email': teacher_user.email,
                    'class_level': lesson_update.class_,
                    'day': lesson_update.day,
                    'subject': lesson_update.subject,
                    'lesson': lesson_update.lesson,
                    'activity': lesson_update.activity,
                    'created_at': lesson_update.created_at.isoformat(),
                    'applicable_children': [
                        {
                            'child_id': child.child_id,
                            'name': f"{Users.query.get(child.user_id).first_name} {Users.query.get(child.user_id).last_name}"
                        }
                        for child in applicable_children
                    ]
                }
                result.append(lesson_data)
            
            # Group by children for easier frontend consumption
            children_with_lessons = []
            for child in linked_children:
                child_user = Users.query.get(child.user_id)
                child_lessons = [
                    lesson for lesson in result 
                    if any(c['child_id'] == child.child_id for c in lesson['applicable_children'])
                ]
                
                children_with_lessons.append({
                    'child_id': child.child_id,
                    'child_name': f"{child_user.first_name} {child_user.last_name}",
                    'class_level': child.class_,
                    'school_name': child.school_name,
                    'streak': child.streak,
                    'xp_points': child.xp_points,
                    'recent_lessons': child_lessons[:10]  # Last 10 lessons
                })
            
            return {
                'children_with_lessons': children_with_lessons,
                'all_lesson_updates': result
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'An error occurred while retrieving lesson updates', 
                'error': str(e)}, 500
