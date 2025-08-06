from datetime import date, datetime, timedelta, timezone

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import func

from models import *
from utils import *


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
            created_at = datetime.now(timezone.utc)

            # Optional fields
            start_date_str = data.get('start_date')  # ISO 8601 string
            due_date_str = data.get('due_date')      # ISO 8601 string
            
            start_date = None
            due_date = None

            # Parse and validate start_date
            if start_date_str:
                try:
                    start_date = datetime.fromisoformat(start_date_str)
                    if start_date < created_at:
                        return {'error': 'Start date cannot be before creation time'}, 400
                except ValueError:
                    return {'error': 'Invalid start_date format. Use ISO 8601 format.'}, 400

            # Parse and validate due_date
            if due_date_str:
                try:
                    due_date = datetime.fromisoformat(due_date_str)
                    if start_date and due_date <= start_date:
                        return {'error': 'Due date must be after start date'}, 400
                except ValueError:
                    return {'error': 'Invalid due_date format. Use ISO 8601 format.'}, 400

            # Create to-do item
            todo_item = ToDoList(
                child_id=child.child_id,
                to_do=to_do,
                description=description,
                is_daily=is_daily,
                created_at=created_at,
                start_date=start_date,
                due_date=due_date
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
                'start_date': todo_item.start_date.isoformat() if todo_item.start_date else None,
                'due_date': todo_item.due_date.isoformat() if todo_item.due_date else None
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
        Returns lesson updates from all teachers linked to the child.
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

            # Get all lesson updates from these teachers
            lesson_updates = LessonUpdates.query.filter(LessonUpdates.teacher_id.in_(teacher_ids)).order_by(LessonUpdates.created_at.desc()).all()

            result = []
            for lesson in lesson_updates:
                teacher = Teacher.query.filter_by(teacher_id=lesson.teacher_id).first()
                teacher_user = Users.query.filter_by(user_id=teacher.user_id).first() if teacher else None
                result.append({
                    'lesson_id': lesson.id,
                    'lesson': lesson.lesson,
                    'summary': lesson.summary,
                    'created_at': lesson.created_at.isoformat(),
                    'teacher_name': f"{teacher_user.first_name} {teacher_user.last_name}" if teacher_user else None
                })

            return {'lesson_updates': result}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


def check_and_update_badges(child_id):
    """
    Check skill achievements and update badges automatically.
    This function should be called whenever a skill is completed.
    """
    try:
        # Get child's skill stats
        total_skills = Skill.query.filter_by(child_id=child_id).count()
        completed_skills = Skill.query.filter_by(child_id=child_id, is_learned=True).count()
        total_skill_xp = db.session.query(func.sum(Skill.skill_xp)).filter_by(
            child_id=child_id, is_learned=True
        ).scalar() or 0

        # Badge criteria and their corresponding achievements
        badge_criteria = [
            # Completion-based badges
            {"name": "First Steps", "level": "bronze", "xp": 10, "condition": completed_skills >= 1},
            {"name": "Skill Builder", "level": "bronze", "xp": 25, "condition": completed_skills >= 5},
            {"name": "Learning Machine", "level": "silver", "xp": 50, "condition": completed_skills >= 10},
            {"name": "Skill Master", "level": "silver", "xp": 100, "condition": completed_skills >= 20},
            {"name": "Expert Learner", "level": "gold", "xp": 200, "condition": completed_skills >= 50},
            
            # XP-based badges
            {"name": "XP Collector", "level": "bronze", "xp": 15, "condition": total_skill_xp >= 100},
            {"name": "XP Hunter", "level": "silver", "xp": 75, "condition": total_skill_xp >= 500},
            {"name": "XP Legend", "level": "gold", "xp": 150, "condition": total_skill_xp >= 1000},
            
            # Completion rate badges
            {"name": "Perfectionist", "level": "gold", "xp": 300, "condition": completed_skills >= 10 and (completed_skills / max(total_skills, 1)) >= 0.9},
        ]

        newly_earned_badges = []
        
        for criteria in badge_criteria:
            if criteria["condition"]:
                # Check if badge already exists
                existing_badge = Badge.query.filter_by(
                    child_id=child_id,
                    badge=criteria["name"],
                    level=criteria["level"]
                ).first()
                
                if not existing_badge:
                    # Create new badge as earned
                    new_badge = Badge(
                        child_id=child_id,
                        badge=criteria["name"],
                        level=criteria["level"],
                        badge_xp=criteria["xp"],
                        is_earned=True,
                        earned_at=datetime.now(timezone.utc)
                    )
                    db.session.add(new_badge)
                    newly_earned_badges.append({
                        'badge': criteria["name"],
                        'level': criteria["level"],
                        'xp': criteria["xp"]
                    })
                elif not existing_badge.is_earned:
                    # Mark existing badge as earned
                    existing_badge.is_earned = True
                    existing_badge.earned_at = datetime.now(timezone.utc)
                    newly_earned_badges.append({
                        'badge': existing_badge.badge,
                        'level': existing_badge.level,
                        'xp': existing_badge.badge_xp
                    })
        
        return newly_earned_badges
    except Exception as e:
        print(f"Error updating badges: {str(e)}")
        return []

class SkillResource(Resource):
    @jwt_required()
    def post(self):
        """Create a new skill for the logged-in child user."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can create skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            data = request.get_json()
            if not data.get('skill_name', '').strip():
                return {'error': 'Skill name is required'}, 400

            # Extract fields
            skill_name = data['skill_name'].strip()
            video_url = data.get('video_url', '').strip() if data.get('video_url') else None
            skill_xp = data.get('skill_xp', 0)

            new_skill = Skill(
                child_id=child.child_id,
                skill_name=skill_name,
                video_url=video_url,
                skill_xp=skill_xp,
                is_learned=False
            )

            db.session.add(new_skill)
            db.session.commit()

            return {
                'message': 'Skill created successfully',
                'skill': new_skill.to_dict()
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def get(self):
        """Get all skills for the logged-in child user with badge information."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can view skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Query parameters
            is_learned = request.args.get('is_learned')
            
            query = Skill.query.filter_by(child_id=child.child_id)
            
            # Filter by completion status
            if is_learned is not None:
                is_learned_bool = is_learned.lower() == 'true'
                query = query.filter_by(is_learned=is_learned_bool)
            
            skills = query.order_by(Skill.created_at.desc()).all()
            
            # Get badge information
            total_badges = Badge.query.filter_by(child_id=child.child_id).count()
            earned_badges = Badge.query.filter_by(child_id=child.child_id, is_earned=True).count()
            recent_badges = Badge.query.filter_by(
                child_id=child.child_id, 
                is_earned=True
            ).order_by(Badge.earned_at.desc()).limit(3).all()
            
            return {
                'skills': [skill.to_dict() for skill in skills],
                'total': len(skills),
                'badge_summary': {
                    'total_badges': total_badges,
                    'earned_badges': earned_badges,
                    'recent_badges': [
                        {
                            'badge': badge.badge,
                            'level': badge.level,
                            'earned_at': badge.earned_at.isoformat()
                        } for badge in recent_badges
                    ]
                }
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def put(self, skill_id):
        """Update a specific skill for the logged-in child user."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can update skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the skill and verify ownership
            skill = Skill.query.filter_by(id=skill_id, child_id=child.child_id).first()

            if not skill:
                return {'error': 'Skill not found or access denied'}, 404

            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400

            was_learned_before = skill.is_learned
            newly_earned_badges = []

            # Update fields if provided
            if 'skill_name' in data and data['skill_name'].strip():
                skill.skill_name = data['skill_name'].strip()
            if 'video_url' in data:
                skill.video_url = data['video_url'].strip() if data['video_url'] else None
            if 'skill_xp' in data:
                skill.skill_xp = data['skill_xp']
            if 'is_learned' in data:
                skill.is_learned = data['is_learned']
                # Set completion date if skill is marked as learned
                if data['is_learned'] and not skill.completion_date:
                    skill.completion_date = datetime.now(timezone.utc)
                    # Check for new badges if skill was just completed
                    if not was_learned_before:
                        newly_earned_badges = check_and_update_badges(child.child_id)
                elif not data['is_learned']:
                    skill.completion_date = None
            
            db.session.commit()
            
            response_data = {
                'message': 'Skill updated successfully',
                'skill': skill.to_dict()
            }
            
            # Include newly earned badges in response
            if newly_earned_badges:
                response_data['newly_earned_badges'] = newly_earned_badges
                response_data['message'] += f' and earned {len(newly_earned_badges)} new badge(s)!'
            
            return response_data, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def delete(self, skill_id):
        """Delete a specific skill for the logged-in child user."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can delete skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the skill and verify ownership
            skill = Skill.query.filter_by(id=skill_id, child_id=child.child_id).first()

            if not skill:
                return {'error': 'Skill not found or access denied'}, 404

            # Store skill details for response before deletion
            skill_details = skill.to_dict()

            # Delete the skill
            db.session.delete(skill)
            db.session.commit()
            
            return {
                'message': 'Skill deleted successfully',
                'deleted_skill': skill_details
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class CompleteSkillResource(Resource):
    @jwt_required()
    def patch(self, skill_id):
        """Mark a skill as completed, add XP, and check for badge updates."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can complete skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            # Find the skill and verify ownership
            skill = Skill.query.filter_by(id=skill_id, child_id=child.child_id).first()

            if not skill:
                return {'error': 'Skill not found or access denied'}, 404

            if skill.is_learned:
                return {'error': 'Skill already completed'}, 400

            data = request.get_json() or {}
            xp_to_add = data.get('xp', 10)  # Default 10 XP for completion
            
            # Mark skill as completed
            skill.is_learned = True
            skill.skill_xp += xp_to_add
            skill.completion_date = datetime.now(timezone.utc)
            
            # Check for newly earned badges
            newly_earned_badges = check_and_update_badges(child.child_id)
            
            db.session.commit()
            
            response_data = {
                'message': 'Skill completed successfully!',
                'skill': skill.to_dict(),
                'xp_earned': xp_to_add
            }
            
            # Include newly earned badges in response
            if newly_earned_badges:
                response_data['newly_earned_badges'] = newly_earned_badges
                response_data['message'] += f' You earned {len(newly_earned_badges)} new badge(s)!'
            
            return response_data, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class SkillStatsResource(Resource):
    @jwt_required()
    def get(self):
        """Get skill statistics with badge information for the logged-in child user."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can view skill stats'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            skills_query = Skill.query.filter_by(child_id=child.child_id)
            
            total_skills = skills_query.count()
            completed_skills = skills_query.filter_by(is_learned=True).count()
            total_xp = db.session.query(func.sum(Skill.skill_xp)).filter_by(child_id=child.child_id).scalar() or 0
            
            # Recent completions (last 7 days)
            week_ago = datetime.now(timezone.utc) - timedelta(days=7)
            recent_completions = skills_query.filter(
                Skill.is_learned == True,
                Skill.completion_date >= week_ago
            ).count()

            # Get recent completed skills (last 5)
            recent_skills = skills_query.filter_by(is_learned=True).order_by(
                Skill.completion_date.desc()
            ).limit(5).all()
            
            # Get badge statistics
            badge_query = Badge.query.filter_by(child_id=child.child_id)
            total_badges = badge_query.count()
            earned_badges = badge_query.filter_by(is_earned=True).count()
            badge_xp = db.session.query(func.sum(Badge.badge_xp)).filter_by(
                child_id=child.child_id, is_earned=True
            ).scalar() or 0
            
            # Recent earned badges (last 3)
            recent_badges = badge_query.filter_by(is_earned=True).order_by(
                Badge.earned_at.desc()
            ).limit(3).all()
            
            return {
                'child_name': user.first_name + ' ' + user.last_name,
                'skills': {
                    'total_skills': total_skills,
                    'completed_skills': completed_skills,
                    'completion_rate': round((completed_skills / total_skills * 100), 1) if total_skills > 0 else 0,
                    'total_xp': total_xp,
                    'recent_completions': recent_completions,
                    'recent_skills': [
                        {
                            'skill_id': skill.id,
                            'skill_name': skill.skill_name,
                            'skill_xp': skill.skill_xp,
                            'completion_date': skill.completion_date.isoformat()
                        } for skill in recent_skills
                    ]
                },
                'badges': {
                    'total_badges': total_badges,
                    'earned_badges': earned_badges,
                    'badge_completion_rate': round((earned_badges / total_badges * 100), 1) if total_badges > 0 else 0,
                    'badge_xp': badge_xp,
                    'recent_badges': [
                        {
                            'badge': badge.badge,
                            'level': badge.level,
                            'badge_xp': badge.badge_xp,
                            'earned_at': badge.earned_at.isoformat()
                        } for badge in recent_badges
                    ]
                },
                'combined_xp': total_xp + badge_xp
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class SkillSearchResource(Resource):
    @jwt_required()
    def get(self):
        """Search skills by name for the logged-in child user."""
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.CHILD).first()

            if not user:
                return {'error': 'Only active child users can search skills'}, 403

            child = Child.query.filter_by(user_id=user.user_id).first()
            if not child:
                return {'error': 'Child profile not found'}, 404

            query_param = request.args.get('q', '')
            
            if not query_param:
                return {'error': 'Search query is required'}, 400
            
            skills = Skill.query.filter(
                Skill.child_id == child.child_id,
                Skill.skill_name.ilike(f'%{query_param}%')
            ).order_by(Skill.created_at.desc()).all()
            
            return {
                'skills': [skill.to_dict() for skill in skills],
                'total': len(skills),
                'query': query_param
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
