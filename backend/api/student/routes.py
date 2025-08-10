from datetime import date, datetime, timedelta, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import func

from models import *
from utils import *

from google.generativeai import GenerativeModel
import google.generativeai as genai
from config import config

GEMINI_API_KEY = config['default'].GEMINI_API_KEY
GEMINI_MODEL = config['default'].GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = GenerativeModel(GEMINI_MODEL)

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
        

class Habits(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new habit for the logged-in child user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can create habits'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            data = request.get_json()
            habit_name = data.get('habit_name', '').strip()
            habit_description = data.get('habit_description', '').strip()
            habit_category = data.get('habit_category', '').strip()
            habit_xp = data.get('habit_xp', 20)  # Default XP points for habit

            if not (habit_name and habit_description and habit_category):
                return {'error': 'Habit name is required'}, 400

            habit = Habit(
                child_id=child.child_id,
                name=habit_name,
                description=habit_description,
                category=habit_category,
                habit_xp=habit_xp,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(habit)
            db.session.commit()

            return {
                'message': 'Habit created successfully',
                'habit_id': habit.id,
                'created_at': habit.created_at.isoformat(),
                'habit_name': habit.name
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def get(self):
        """
        Get all habits for the logged-in child user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can view habits'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            habits = Habit.query.filter_by(child_id=child.child_id).all()

            completed_habits = HabitCompletion.query.filter_by(child_id=child.child_id).all()

            if not habits:
                return {'message': 'No habits found for this child'}, 200

            return {
                'habits_created': [
                    {
                        'habit_id': habit.id,
                        'name': habit.name,
                        'description': habit.description,
                        'category': habit.category,
                        'created_at': habit.created_at.isoformat(),
                        # 'completion_date': habit.completion_date.isoformat() if habit.completion_date else None
                    } for habit in habits
                ],
                'completed_habits': [
                    {
                        'habit_id': completion.habit_id,
                        'is_done': completion.is_done,
                        'completion_date': completion.completion_date.isoformat() if completion.completion_date else None
                    } for completion in completed_habits
                ]
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def put(self, habit_id):
        """
        Update a specific habit for the logged-in child user.
        URL: /habits/<int:habit_id>
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can update habits'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the habit and verify ownership
            habit = Habit.query.filter_by(id=habit_id, child_id=child.child_id).first()

            if not habit:
                return {'error': 'Habit not found or access denied'}, 404

            data = request.get_json()
            habit_name = data.get('habit_name', '').strip()
            habit_description = data.get('habit_description', '').strip()
            habit_category = data.get('habit_category', '').strip()
            habit_xp = data.get('habit_xp')

            if not (habit_name and habit_description and habit_category):
                return {'error': 'Habit name is required'}, 400

            # Update the habit
            habit.name = habit_name
            habit.description = habit_description
            habit.category = habit_category
            habit.habit_xp = habit_xp if habit_xp is not None else habit.habit_xp
            habit.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()

            return {
                'message': 'Habit updated successfully',
                'habit_id': habit.id,
                'created_at': habit.created_at.isoformat(),
                'updated_at': habit.updated_at.isoformat(),
                'habit_name': habit.name
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def delete(self, habit_id):
        """
        Delete a specific habit for the logged-in child user.
        URL: /habits/<int:habit_id>
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can delete habits'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the habit and verify ownership
            habit = Habit.query.filter_by(id=habit_id, child_id=child.child_id).first()

            habit_completion = HabitCompletion.query.filter_by(
                child_id=child.child_id,
                habit_id=habit_id
            ).all()

            if not habit:
                return {'error': 'Habit not found or access denied'}, 404

            # Store habit details for response before deletion
            habit_details = {
                'habit_id': habit.id,
                'created_at': habit.created_at.isoformat(),
                'name': habit.name,
                'description': habit.description,
                'category': habit.category
            }

            # Delete the habit
            db.session.delete(habit)
            db.session.delete(habit_completion) if habit_completion else None
            db.session.commit()

            return {
                'message': 'Habit deleted successfully',
                'deleted_habit': habit_details
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class CompleteHabit(Resource):
    @jwt_required()
    def post(self, habit_id):
        """
        Mark a habit as done for the logged-in child user.
        URL: /habits/<int:habit_id>/complete
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can mark habits as done'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the habit and verify ownership
            habit = Habit.query.filter_by(id=habit_id, child_id=child.child_id).first()

            if not habit:
                return {'error': 'Habit not found or access denied'}, 404
            
            # check if habit is already completed today
            habit_completion = HabitCompletion.query.filter_by(
                child_id=child.child_id,
                habit_id=habit.id,
                completion_date=date.today()
            ).first()
            
            if habit_completion:
                if habit_completion.completion_date and habit_completion.completion_date == date.today():
                    return {'error': 'Habit already completed today'}, 400

            habit_completion = HabitCompletion(
                child_id=child.child_id,
                habit_id=habit.id,
                is_done=True,
                completion_date=date.today()
            )
            db.session.add(habit_completion)
            db.session.commit()
            return {'message': 'Habit done successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500



class ToDoListResource(Resource):
    """Manage to-do list items."""
    @jwt_required()
    def post(self):
        """Create a new to-do item."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            
            if not user:
                return {'error': 'Only active child users can create to-do items'}, 403
            
            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['to_do', 'description']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400
            
            to_do = data['to_do'].strip()
            description = data['description'].strip()
            is_daily = data.get('is_daily', False)
            is_done = data.get('is_done', False)
            created_at = datetime.now(timezone.utc)

            # Optional fields
            completion_date_str = data.get('completion_date')      # ISO 8601 string
            
            completion_date = None


            # Create to-do item
            todo_item = ToDoList(
                child_id=child.child_id,
                to_do=to_do,
                description=description,
                is_daily=is_daily,
                is_done=is_done,
                created_at=created_at,
                completion_date=completion_date
            )
            
            db.session.add(todo_item)
            db.session.commit()
            
            response_data = {
                'message': 'To-do item created successfully',
                'list_id': todo_item.list_id,
                'to_do': todo_item.to_do,
                'description': todo_item.description,
                'is_daily': todo_item.is_daily,
                'is_done': todo_item.is_done,
                'created_at': todo_item.created_at.isoformat(),
                'completion_date': todo_item.completion_date.isoformat() if todo_item.completion_date else None
            }
            
            return response_data, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    
    @jwt_required()
    def get(self):
        """Get to-do items for the logged-in child."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            
            if not user:
                return {'error': 'Only active child users can view to-do items'}, 403
            
            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404
            
            # Query parameters
            is_done = request.args.get('is_done')
            is_daily = request.args.get('is_daily')
            date_str = request.args.get('date')
            
            query = ToDoList.query.filter_by(child_id=child.child_id)
            
            # Filter by completion status
            if is_done is not None:
                is_done_bool = is_done.lower() == 'true'
                query = query.filter_by(is_done=is_done_bool)
            
            # Filter by daily tasks
            if is_daily is not None:
                is_daily_bool = is_daily.lower() == 'true'
                query = query.filter_by(is_daily=is_daily_bool)
            
            # Filter by date
            if date_str:
                try:
                    target_date = datetime.strptime(date_str, "%d-%m-%y").date()
                    query = query.filter(func.date(ToDoList.created_at) == target_date)
                except ValueError:
                    return {'error': 'Invalid date format. Use DD-MM-YY'}, 400
            
            todos = query.order_by(ToDoList.created_at.desc()).all()
            
            return {
                'todos': [
                    {
                        'list_id': todo.list_id,
                        'to_do': todo.to_do,
                        'description': todo.description,
                        'is_done': todo.is_done,
                        'is_daily': todo.is_daily,
                        'is_done': todo.is_done,
                        'created_at': todo.created_at.isoformat(),
                        'completion_date': todo.completion_date.isoformat() if todo.completion_date else None
                    } for todo in todos
                ]
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def put(self, todo_id):
        """Update a to-do item."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            
            if not user:
                return {'error': 'Only active child users can update to-do items'}, 403
            
            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404
            
            data = request.get_json()
            list_id = data.get('list_id')
            
            if not list_id:
                return {'error': 'list_id is required'}, 400
            
            todo_item = ToDoList.query.filter_by(list_id=list_id, child_id=child.child_id).first()
            if not todo_item:
                return {'error': 'To-do item not found'}, 404
            
            # Update fields
            if 'to_do' in data:
                todo_item.to_do = data['to_do'].strip()
            if 'description' in data:
                todo_item.description = data['description'].strip()
            if 'is_daily' in data:
                todo_item.is_daily = data['is_daily']
            if 'is_done' in data:
                todo_item.is_done = data['is_done']
                if data['is_done'] and not todo_item.completion_date:
                    todo_item.completion_date = datetime.now(timezone.utc)
                elif not data['is_done']:
                    todo_item.completion_date = None
            
            db.session.commit()
            
            return {
                'message': 'To-do item updated successfully',
                'list_id': todo_item.list_id,
                'to_do': todo_item.to_do,
                'description': todo_item.description,
                'is_done': todo_item.is_done,
                'is_daily': todo_item.is_daily,
                'completion_date': todo_item.completion_date.isoformat() if todo_item.completion_date else None
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
        
    @jwt_required()
    def delete(self, todo_id):
        """Delete a to-do item."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            
            if not user:
                return {'error': 'Only active child users can delete to-do items'}, 403
            
            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404
            
            todo_item = ToDoList.query.filter_by(list_id=todo_id, child_id=child.child_id).first()
            if not todo_item:
                return {'error': 'To-do item not found'}, 404
            
            db.session.delete(todo_item)
            db.session.commit()
            
            return {'message': 'To-do item deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500



class StudentLessonUpdates(Resource):
    @jwt_required()
    def get(self):
        """
        Get all lesson updates for the logged-in child user.
        Returns lesson updates from teachers linked to the child, filtered by the child's class level.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            if not user:
                return {'error': 'Only active child users can view lesson updates'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Get all teachers linked to this child
            teacher_links = TeacherChild.query.filter_by(child_id=child.child_id).all()
            teacher_ids = [link.teacher_id for link in teacher_links]

            if not teacher_ids:
                return {'message': 'No teachers linked to this child.'}, 200

            # Get lesson updates from linked teachers, filtered by child's class level
            query = LessonUpdates.query.filter(LessonUpdates.teacher_id.in_(teacher_ids))
            
            # Filter by child's class if the child has a class assigned
            if child.class_:
                query = query.filter(LessonUpdates.class_ == child.class_)
            
            lesson_updates = query.order_by(LessonUpdates.created_at.desc()).all()

            result = []
            for lesson in lesson_updates:
                teacher = Teacher.query.filter_by(teacher_id=lesson.teacher_id).first()
                teacher_user = Users.query.filter_by(user_id=teacher.user_id).first() if teacher else None
                result.append({
                    'lesson_id': lesson.id,
                    'day': lesson.day,
                    'subject': lesson.subject,
                    'lesson': lesson.lesson,
                    'activity': lesson.activity,
                    'class': lesson.class_,
                    'created_at': lesson.created_at.isoformat(),
                    'teacher_name': f"{teacher_user.first_name} {teacher_user.last_name}" if teacher_user else None
                })

            return {'lesson_updates': result}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class Skills(Resource):
    @jwt_required()
    def get(self):
        """
        Get all skills for the logged-in child user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()
            if not user:
                return {'error': 'Only active child users can view skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Get all common skills
            common_skills = CommonSkill.query.all()
            if not common_skills:
                return {'message': 'No skills found'}, 200
            skills = []
            for skill in common_skills:
                skill_data = {
                    'id': skill.id,
                    'skill_name': skill.skill_name,
                    'video_url': skill.video_url,
                    'skill_xp': skill.skill_xp,
                    'created_at': skill.created_at.isoformat(),
                    'is_learned': None
                }
                
                # Check if the child has learned this skill
                child_skill = SkillCompleted.query.filter_by(child_id=child.child_id, skill_id=skill.id).first()
                if child_skill:
                    skill_data['is_learned'] = child_skill.is_learned
                    skill_data['completion_date'] = child_skill.completion_date.isoformat() if child_skill.completion_date else None
                
                skills.append(skill_data)
            return {'skills': skills}, 200
        
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def post(self):
        """
        Add a new skill to the common skills list.
        Teacher and Principal can add common skills
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True).first()
            if not user:
                return {'error': 'User not found or inactive'}, 404
            
            # Check if user is a teacher or principal
            if not user or user.role_type not in [UserRole.TEACHER, UserRole.PRINCIPAL]:
                return {'error': 'Only teachers and principals can add skills'}, 403
            
            # Validate request data
            data = request.get_json()
            skill_name = data.get('skill_name', '').strip()
            video_url = data.get('video_url', '').strip()
            skill_xp = data.get('skill_xp')

            if not skill_name or not video_url:
                return {'error': 'Skill name and video URL are required'}, 400
            
            if not isinstance(skill_xp, int) or skill_xp <= 0:
                return {'error': 'Skill XP must be a positive integer'}, 400
            
            # Check if skill already exists
            existing_skill = CommonSkill.query.filter_by(skill_name=skill_name).first()
            if existing_skill:
                return {'error': 'Skill already exists'}, 400
            
            # Create new skill
            new_skill = CommonSkill(
                skill_name=skill_name,
                video_url=video_url,
                skill_xp=skill_xp,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(new_skill)
            db.session.commit()
            return {'message': 'Skill added successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def put(self, skill_id):
        """
        Update an existing skill.
        Teacher and Principal can update common skills
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True).first()
            if not user:
                return {'error': 'User not found or inactive'}, 404
            
            # Check if user is a teacher or principal
            if not user or user.role_type not in [UserRole.TEACHER, UserRole.PRINCIPAL]:
                return {'error': 'Only teachers and principals can update skills'}, 403
            
            # Validate request data
            data = request.get_json()
            skill_name = data.get('skill_name', '').strip()
            video_url = data.get('video_url', '').strip()
            skill_xp = data.get('skill_xp')

            if not skill_name or not video_url:
                return {'error': 'Skill name and video URL are required'}, 400
            
            if not isinstance(skill_xp, int) or skill_xp <= 0:
                return {'error': 'Skill XP must be a positive integer'}, 400
            
            # Find the skill to update
            skill = CommonSkill.query.filter_by(id=skill_id).first()
            if not skill:
                return {'error': 'Skill not found'}, 404
            
            # Update the skill
            skill.skill_name = skill_name
            skill.video_url = video_url
            skill.skill_xp = skill_xp
            db.session.commit()
            
            return {'message': 'Skill updated successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
    
    @jwt_required()
    def delete(self, skill_id):
        """
        Delete a skill.
        Teacher and Principal can delete common skills
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True).first()
            if not user:
                return {'error': 'User not found or inactive'}, 404

            # Check if user is a teacher or principal
            if not user or user.role_type not in [UserRole.TEACHER, UserRole.PRINCIPAL]:
                return {'error': 'Only teachers and principals can delete skills'}, 403

            # Find the skill to delete
            skill = CommonSkill.query.filter_by(id=skill_id).first()
            if not skill:
                return {'error': 'Skill not found'}, 404

            db.session.delete(skill)
            db.session.commit()

            return {'message': 'Skill deleted successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class CompleteSkill(Resource):
    @jwt_required()
    def post(self, skill_id):
        """
        Mark a skill as learned by the logged-in child user.
        URL: /skills/<int:skill_id>/complete
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can mark skills as learned'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the skill and verify ownership
            skill = CommonSkill.query.filter_by(id=skill_id).first()

            if not skill:
                return {'error': 'Skill not found or access denied'}, 404
            
            # Check if the skill is already marked as learned
            existing_skill = SkillCompleted.query.filter_by(
                child_id=child.child_id,
                skill_id=skill.id
            ).first()
            
            if existing_skill and existing_skill.is_learned:
                return {'error': 'Skill already marked as learned'}, 400

            # Create or update the skill completion record
            if existing_skill:
                existing_skill.is_learned = True
                existing_skill.completion_date = datetime.now(timezone.utc)
                db.session.add(existing_skill)
            else:
                new_skill_completion = SkillCompleted(
                    child_id=child.child_id,
                    skill_id=skill.id,
                    is_learned=True,
                    completion_date=datetime.now(timezone.utc)
                )
                db.session.add(new_skill_completion)

            db.session.commit()
            return {'message': 'Skill marked as learned successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500
    

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        """
        Get the profile of the logged-in child user.
        Returns basic information about the child user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can view their profile'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            profile_data = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'child_id': child.child_id,
                'dob': child.dob.isoformat() if child.dob else None,
                'gender': child.gender,
                'class_level': child.class_,
                'created_at': child.created_at.isoformat(),
                'unique_key': child.unique_key,
                'school_name': child.school_name,
                'streak': child.streak,
                'xp_points': child.xp_points,
                'is_linked': child.is_linked,
            }
            
            return {'profile': profile_data}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class CommunicationHelper:
    def __init__(self):
        self.grammar_patterns = {
            # Common grammar issues
            'had_to_have': r'\b(have|has)\s+had\s+to\b',
            'double_past': r'\b(told|said|asked)\s+.*\s+(have|has)\s+had\b',
            'tense_consistency': r'\b(yesterday|last)\s+.*\s+(have|has)\b',
            'redundant_that': r'\bthat\s+that\b',
            'run_on': r'^[^.!?]{100,}$'  # Very long sentences without punctuation
        }
        
        # Child-friendly encouragement phrases
        self.encouragements = [
            "Great job trying!",
            "You're doing awesome!",
            "Nice work!",
            "Keep it up, superstar!",
            "You're getting better every day!",
            "Fantastic effort!",
            "Way to go!",
            "You're a writing champion!"
        ]
        
        self.positive_starters = [
            "Wow, this is a great start!",
            "I love your creativity!",
            "You have some really cool ideas here!",
            "This is coming along nicely!",
            "You're thinking like a real writer!"
        ]
    
    def get_child_friendly_encouragement(self):
        """Get a random encouraging phrase for kids"""
        import random
        return random.choice(self.encouragements)
    
    def get_positive_starter(self):
        """Get a positive conversation starter"""
        import random
        return random.choice(self.positive_starters)
    
    def analyze_sentence(self, sentence):
        """Analyze sentence for common issues - child-friendly version"""
        issues = []
        suggestions = []
        
        # Check for grammar patterns with kid-friendly language
        if re.search(self.grammar_patterns['tense_consistency'], sentence, re.IGNORECASE):
            issues.append("Let's check when things happened - past or present?")
            suggestions.append("Try using the same time (past or present) throughout your sentence")
        
        if re.search(self.grammar_patterns['double_past'], sentence, re.IGNORECASE):
            issues.append("We might be mixing up our past tenses")
            suggestions.append("Pick one way to talk about the past and stick with it")
        
        if re.search(self.grammar_patterns['redundant_that'], sentence, re.IGNORECASE):
            issues.append("Looks like 'that' appears twice - we only need it once!")
            suggestions.append("Remove the extra 'that' word")
        
        if re.search(self.grammar_patterns['run_on'], sentence):
            issues.append("This sentence is getting pretty long!")
            suggestions.append("Try breaking it into 2 or 3 shorter sentences - it'll be easier to read!")
        
        # Check sentence length and complexity
        word_count = len(sentence.split())
        if word_count > 25:
            issues.append("This sentence has lots of words!")
            suggestions.append("Let's split this into smaller sentences so it's easier to understand")
        
        return issues, suggestions

    def improve_sentence_with_ai(self, sentence):
        """Use AI to improve the sentence - child-friendly version"""
        try:
            prompt = f"""
            You are helping a child aged 8-14 improve their writing. Be encouraging, positive, and use simple language.
            
            Please help improve this sentence: "{sentence}"
            
            Provide:
            1. An improved version that keeps their original idea
            2. A simple, encouraging explanation of what you changed (use kid-friendly language)
            3. One fun tip to remember for next time
            
            Be very positive and encouraging. Start with praise for their effort!
            Keep the language simple and age-appropriate for children 8-14.
            Make it sound like a helpful friend, not a teacher.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"{self.get_child_friendly_encouragement()} I'm having trouble right now, but your sentence looks great! Keep practicing!"

    def get_speaking_tips(self, text_type="general"):
        """Get kid-friendly speaking tips"""
        tips = {
            "general": [
                "Take your time - there's no rush! 🌟",
                "Take deep breaths between sentences",
                "Look at your audience and smile 😊",
                "Practice tricky words a few times before speaking"
            ],
            "presentation": [
                "Start by saying hello and introducing yourself",
                "Use words like 'first,' 'next,' and 'finally' to organize your ideas",
                "End with something exciting or interesting",
                "Practice in front of a mirror or with family first!"
            ],
            "conversation": [
                "Ask questions like 'What do you think?' or 'How about you?'",
                "Listen carefully when others speak",
                "Use a voice that everyone can hear clearly",
                "Show you're interested by nodding and looking at the speaker"
            ],
            "story": [
                "Use exciting words to describe characters and places",
                "Make your voice change for different characters",
                "Pause at exciting parts to build suspense",
                "Don't forget to have fun telling your story!"
            ]
        }
        return tips.get(text_type, tips["general"])

    def analyze_writing(self, text, writing_type="general"):
        """Analyze longer writing pieces - child-friendly version"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        analysis = {
            "sentence_count": len(sentences),
            "word_count": len(text.split()),
            "avg_sentence_length": len(text.split()) / max(len(sentences), 1),
            "issues": [],
            "suggestions": [],
            "praise_points": []  # Added praise points for kids
        }
        
        # Add praise points based on what they did well
        if analysis["sentence_count"] >= 3:
            analysis["praise_points"].append("You wrote multiple sentences - great storytelling!")
        
        if analysis["word_count"] > 20:
            analysis["praise_points"].append("Wow, you used lots of words to express your ideas!")
        
        if writing_type == "story" and any(word in text.lower() for word in ['once', 'then', 'finally', 'suddenly']):
            analysis["praise_points"].append("You used great story words to connect your ideas!")
        
        # Check each sentence with encouraging language
        for i, sentence in enumerate(sentences):
            issues, suggestions = self.analyze_sentence(sentence)
            if issues:
                analysis["issues"].extend([f"In sentence {i+1}: {issue}" for issue in issues])
                analysis["suggestions"].extend(suggestions)
        
        # Overall writing suggestions with positive framing
        if analysis["avg_sentence_length"] > 20:
            analysis["suggestions"].append("Try using shorter sentences - they're easier to read and understand!")
        
        if analysis["sentence_count"] < 3 and analysis["word_count"] > 50:
            analysis["suggestions"].append("You have great ideas! Try breaking them into more sentences.")
        
        return analysis

communication_helper = CommunicationHelper()


class ImproveSentence(Resource):
    @jwt_required()
    def post(self):
        """
        Improve a sentence using AI - child-friendly version.
        URL: /improve-sentence
        """
        try:
            data = request.get_json()
            if not data or 'sentence' not in data:
                return {"error": "Please share a sentence you'd like help with!"}, 400
            
            sentence = data['sentence'].strip()
            if not sentence:
                return {"error": "Oops! The sentence seems to be empty. Try typing something!"}, 400
            
            # Basic analysis
            issues, suggestions = communication_helper.analyze_sentence(sentence)
            
            # AI improvement
            ai_improvement = communication_helper.improve_sentence_with_ai(sentence)
            
            # Speaking tips
            speaking_tips = communication_helper.get_speaking_tips("general")
            
            # Add encouragement
            encouragement = communication_helper.get_child_friendly_encouragement()
            
            return {
                "original_sentence": sentence,
                "issues": issues,
                "suggestions": suggestions,
                "ai_improvement": ai_improvement,
                "speaking_tips": speaking_tips[:3],
                "word_count": len(sentence.split()),
                "encouragement": encouragement,
                "fun_fact": "Did you know? The average sentence has about 15-20 words!"
            }
        
        except Exception as e:
            return {"error": "Oops! Something went wrong, but keep trying - you're doing great!"}, 500

class AnalyzeWriting(Resource):
    @jwt_required()
    def post(self):
        """Analyze longer writing pieces - child-friendly version"""
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                return {"error": "Please share your writing so I can help make it even better!"}, 400
            
            text = data['text'].strip()
            writing_type = data.get('type', 'story')  # Default to story for kids
            
            if not text:
                return {"error": "It looks like you haven't written anything yet. Give it a try!"}, 400
            
            # Analyze the writing
            analysis = communication_helper.analyze_writing(text, writing_type)
            
            # Get AI feedback with child-friendly prompting
            try:
                feedback_prompt = f"""
                You are helping a child aged 8-14 improve their {writing_type}. Be very encouraging and positive!
                
                Here's what they wrote: "{text}"
                
                Please provide feedback that:
                1. Starts with genuine praise for what they did well (be specific!)
                2. Gives 2-3 gentle suggestions for improvement using simple, friendly language
                3. Encourages them to keep writing and practicing
                4. Includes one fun writing tip they can try next time
                
                Use encouraging language like "Great job!", "I love how you...", "You're really good at..."
                Keep suggestions positive: "You could try..." instead of "You should fix..."
                Make it sound like a helpful friend, not a teacher grading their work.
                Use simple words and short sentences.
                """
                
                ai_response = model.generate_content(feedback_prompt)
                ai_feedback = ai_response.text
            except Exception as e:
                ai_feedback = f"{communication_helper.get_positive_starter()} Your writing shows great imagination! Keep practicing and you'll get even better!"
            
            # Speaking tips for this type of writing
            speaking_tips = communication_helper.get_speaking_tips(writing_type)
            
            # Fun writing badges based on their work
            badges = []
            if analysis["word_count"] > 50:
                badges.append("📝 Word Champion")
            if analysis["sentence_count"] > 5:
                badges.append("⭐ Sentence Star")
            if writing_type == "story":
                badges.append("📚 Storyteller")
            
            return {
                "analysis": analysis,
                "ai_feedback": ai_feedback,
                "speaking_tips": speaking_tips,
                "writing_type": writing_type,
                "readability_score": "Perfect for your age!" if analysis["avg_sentence_length"] < 20 else "Great job! Try shorter sentences next time",
                "badges_earned": badges,
                "encouragement": communication_helper.get_child_friendly_encouragement()
            }
        
        except Exception as e:
            return {"error": "Something went wrong, but your writing is awesome! Keep it up!"}, 500
