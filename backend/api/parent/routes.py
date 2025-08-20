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
            
            # Check if child is already linked to this parent
            existing_link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, 
                child_id=child.child_id
            ).first()
            if existing_link:
                return {'message': 'Child is already linked to your account'}, 400
            
            # Check if child is actually linked to any parent (check the actual relationships)
            any_existing_link = ParentChild.query.filter_by(child_id=child.child_id).first()
            if any_existing_link:
                return {'message': 'Child is already linked to another parent'}, 400
            
            # Create the link
            link = ParentChild(
                parent_id=parent.parent_id,
                child_id=child.child_id,
                linked_at=datetime.utcnow()
            )
            db.session.add(link)
            
            # Ensure the is_linked flag is set correctly
            child.is_linked = True
            
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


class ChildHabitsAPI(Resource):
    @jwt_required()
    def get(self, child_id):
        """
        Get detailed habits data for a specific child.
        Only accessible by the child's linked parent.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'error': 'Parent not found'}, 404

            # Verify parent is linked to the child
            link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, child_id=child_id
            ).first()
            if not link:
                return {'error': 'Child is not linked to this parent'}, 404

            habits = Habit.query.filter_by(child_id=child_id).all()
            habits_data = []
            
            for habit in habits:
                # Get completion history (last 30 days)
                completions = HabitCompletion.query.filter(
                    HabitCompletion.habit_id == habit.id,
                    HabitCompletion.completion_date >= (datetime.now() - timedelta(days=30))
                ).order_by(HabitCompletion.completion_date.desc()).all()
                
                completion_history = []
                for completion in completions:
                    completion_history.append({
                        'completion_date': completion.completion_date.isoformat(),
                        'is_done': completion.is_done
                    })
                
                habits_data.append({
                    'habit_id': habit.id,
                    'name': habit.name,
                    'description': habit.description,
                    'category': habit.category,
                    'habit_xp': habit.habit_xp,
                    'completion_history': completion_history,
                    'total_completions': len([c for c in completion_history if c['is_done']])
                })

            return {'habits': habits_data}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ChildSkillsAPI(Resource):
    @jwt_required()
    def get(self, child_id):
        """
        Get detailed skills data for a specific child.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'error': 'Parent not found'}, 404

            # Verify parent is linked to the child
            link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, child_id=child_id
            ).first()
            if not link:
                return {'error': 'Child is not linked to this parent'}, 404

            # Get all skills with completion status
            skills = db.session.query(CommonSkill, SkillCompleted).outerjoin(
                SkillCompleted, (CommonSkill.id == SkillCompleted.skill_id) & 
                (SkillCompleted.child_id == child_id)
            ).all()
            
            # Since skill_type column doesn't exist, group all skills under 'general'
            skills_by_type = {'general': []}
            for skill, completion in skills:
                skills_by_type['general'].append({
                    'skill_id': skill.id,
                    'skill_name': skill.skill_name,
                    'skill_xp': skill.skill_xp,
                    'video_url': skill.video_url,
                    'is_completed': completion.is_learned if completion else False,
                    'completion_date': completion.completion_date.isoformat() if completion and completion.completion_date else None
                })

            return {'skills_by_type': skills_by_type}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ChildBadgesAPI(Resource):
    @jwt_required()
    def get(self, child_id):
        """
        Get badges earned by a specific child.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'error': 'Parent not found'}, 404

            # Verify parent is linked to the child
            link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, child_id=child_id
            ).first()
            if not link:
                return {'error': 'Child is not linked to this parent'}, 404

            # Get child information
            child = Child.query.get(child_id)
            if not child:
                return {'error': 'Child not found'}, 404
            
            child_user = Users.query.get(child.user_id)
            if not child_user:
                return {'error': 'Child user information not found'}, 404

            badges = Badge.query.filter_by(child_id=child_id, is_earned=True).order_by(
                Badge.earned_at.desc()
            ).all()
            
            badges_data = []
            for badge in badges:
                badges_data.append({
                    'badge_id': badge.id,
                    'badge_name': badge.badge,
                    'description': f"Earned {badge.badge} at level {badge.level}",
                    'badge_type': 'achievement',
                    'icon': '🏆',
                    'level': badge.level,
                    'badge_xp': badge.badge_xp,
                    'earned_at': badge.earned_at.isoformat() if badge.earned_at else None
                })

            # Include child information in response
            child_data = {
                'child_id': child.child_id,
                'name': f"{child_user.first_name} {child_user.last_name}",
                'xp_points': child.xp_points or 0,
                'streak': child.streak or 0
            }

            return {
                'child': child_data,
                'badges': badges_data
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ChildTodosAPI(Resource):
    @jwt_required()
    def get(self, child_id):
        """
        Get todos for a specific child.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'error': 'Parent not found'}, 404

            # Verify parent is linked to the child
            link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, child_id=child_id
            ).first()
            if not link:
                return {'error': 'Child is not linked to this parent'}, 404

            todos = ToDoList.query.filter_by(child_id=child_id).order_by(
                ToDoList.created_at.desc()
            ).all()
            
            todos_data = []
            for todo in todos:
                todos_data.append({
                    'todo_id': todo.list_id,
                    'to_do': todo.to_do,
                    'description': todo.description,
                    'is_done': todo.is_done,
                    'is_daily': todo.is_daily,
                    'created_at': todo.created_at.isoformat(),
                })

            return {'todos': todos_data}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class ChildWeeklyReportAPI(Resource):
    @jwt_required()
    def get(self, child_id):
        """
        Get weekly progress report for a specific child.
        """
        try:
            user_id = get_jwt_identity()
            parent = Parent.query.filter_by(user_id=user_id).first()
            if not parent:
                return {'error': 'Parent not found'}, 404

            # Verify parent is linked to the child
            link = ParentChild.query.filter_by(
                parent_id=parent.parent_id, child_id=child_id
            ).first()
            if not link:
                return {'error': 'Child is not linked to this parent'}, 404

            child = Child.query.get(child_id)
            if not child:
                return {'error': 'Child not found'}, 404

            # Calculate week dates
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            # Get weekly stats
            habits_completed_this_week = HabitCompletion.query.filter(
                HabitCompletion.habit_id.in_(
                    [h.id for h in Habit.query.filter_by(child_id=child_id).all()]
                ),
                HabitCompletion.completion_date >= week_start,
                HabitCompletion.completion_date <= week_end,
                HabitCompletion.is_done == True
            ).count()

            skills_completed_this_week = SkillCompleted.query.filter(
                SkillCompleted.child_id == child_id,
                SkillCompleted.completion_date >= week_start,
                SkillCompleted.completion_date <= week_end,
                SkillCompleted.is_learned == True
            ).count()

            badges_earned_this_week = Badge.query.filter(
                Badge.child_id == child_id,
                Badge.earned_at >= week_start,
                Badge.earned_at <= week_end,
                Badge.is_earned == True
            ).count()

            todos_completed_this_week = ToDoList.query.filter(
                ToDoList.child_id == child_id,
                ToDoList.completion_date >= week_start,
                ToDoList.completion_date <= week_end,
                ToDoList.is_done == True
            ).count()

            return {
                'child_info': {
                    'child_id': child.child_id,
                    'name': f"{child.user.first_name} {child.user.last_name}",
                    'xp_points': child.xp_points,
                    'streak': child.streak
                },
                'week_period': {
                    'start_date': week_start.isoformat(),
                    'end_date': week_end.isoformat()
                },
                'weekly_stats': {
                    'habits_completed': habits_completed_this_week,
                    'skills_completed': skills_completed_this_week,
                    'badges_earned': badges_earned_this_week,
                    'todos_completed': todos_completed_this_week
                }
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
