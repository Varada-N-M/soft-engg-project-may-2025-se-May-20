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
    