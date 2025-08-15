from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models import *
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import and_, desc


def get_overview_dashboard():
    """
    Comprehensive overview API that returns all key metrics and trends
    """
    try:
        # Basic counts
        total_users = Users.query.count()
        total_students = Users.query.filter_by(role_type='CHILD').count()
        total_teachers = Users.query.filter_by(role_type='TEACHER').count()
        total_parents = Users.query.filter_by(role_type='PARENT').count()
        total_schools = School.query.count()
        total_organizations = Organization.query.count()
        
        # Active users (assuming active means created within last 30 days or has recent activity)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_students = Users.query.filter(
            and_(Users.role_type == 'CHILD', Users.created_at >= thirty_days_ago)
        ).count()
        
        # Student engagement metrics
        total_habits = Habit.query.count()
        total_habit_completions = HabitCompletion.query.filter_by(is_done=True).count()
        total_skills = CommonSkill.query.count()
        total_skills_learned = SkillCompleted.query.filter_by(is_learned=True).count()
        total_badges_earned = Badge.query.filter_by(is_earned=True).count()
        total_todos = ToDoList.query.count()
        total_todos_completed = ToDoList.query.filter_by(is_done=True).count()
        total_gratitude_entries = GratitudeEntries.query.count()
        
        # Top performing students (by XP points)
        top_students = db.session.query(
            Child.child_id,
            Users.first_name,
            Users.last_name,
            Child.xp_points,
            Child.streak,
            Child.class_,
            Child.school_name
        ).join(Users, Child.user_id == Users.user_id)\
         .order_by(desc(Child.xp_points))\
         .limit(10).all()
        
        top_students_data = [{
            'child_id': student.child_id,
            'name': f"{student.first_name} {student.last_name}",
            'xp_points': student.xp_points,
            'streak': student.streak,
            'class': student.class_,
            'school': student.school_name
        } for student in top_students]
        
        # Habit completion trends (last 7 days)
        habit_trends = []
        for i in range(7):
            date = (datetime.utcnow() - timedelta(days=i)).date()
            completions = HabitCompletion.query.filter(
                and_(HabitCompletion.completion_date == date, HabitCompletion.is_done == True)
            ).count()
            habit_trends.append({
                'date': date.isoformat(),
                'completions': completions
            })
        
        # Most popular skills
        popular_skills = db.session.query(
            CommonSkill.skill_name,
            CommonSkill.skill_type,
            func.count(SkillCompleted.id).label('learned_count')
        ).join(SkillCompleted, CommonSkill.id == SkillCompleted.skill_id)\
         .filter(SkillCompleted.is_learned == True)\
         .group_by(CommonSkill.id)\
         .order_by(desc('learned_count'))\
         .limit(10).all()
        
        popular_skills_data = [{
            'skill_name': skill.skill_name,
            'skill_type': skill.skill_type,
            'learned_count': skill.learned_count
        } for skill in popular_skills]
        
        # Badge distribution
        badge_stats = db.session.query(
            Badge.badge,
            func.count(Badge.id).label('earned_count')
        ).filter(Badge.is_earned == True)\
         .group_by(Badge.badge)\
         .order_by(desc('earned_count')).all()
        
        badge_distribution = [{
            'badge_name': badge.badge,
            'earned_count': badge.earned_count
        } for badge in badge_stats]
        
        # Habit categories popularity
        habit_categories = db.session.query(
            Habit.category,
            func.count(Habit.id).label('habit_count')
        ).group_by(Habit.category)\
         .order_by(desc('habit_count')).all()
        
        habit_category_data = [{
            'category': cat.category if cat.category else 'Uncategorized',
            'count': cat.habit_count
        } for cat in habit_categories]
        
        # Class-wise distribution
        class_distribution = db.session.query(
            Child.class_,
            func.count(Child.child_id).label('student_count')
        ).filter(Child.class_.isnot(None))\
         .group_by(Child.class_)\
         .order_by(Child.class_).all()
        
        class_data = [{
            'class': cls.class_,
            'student_count': cls.student_count
        } for cls in class_distribution]
        
        # Gender distribution
        gender_distribution = db.session.query(
            Child.gender,
            func.count(Child.child_id).label('count')
        ).filter(Child.gender.isnot(None))\
         .group_by(Child.gender).all()
        
        gender_data = [{
            'gender': gender.gender,
            'count': gender.count
        } for gender in gender_distribution]
        
        # Recent lesson updates
        recent_lessons = db.session.query(
            LessonUpdates.lesson,
            LessonUpdates.subject,
            LessonUpdates.class_,
            LessonUpdates.day,
            LessonUpdates.created_at,
            Users.first_name,
            Users.last_name
        ).join(Teacher, LessonUpdates.teacher_id == Teacher.teacher_id)\
         .join(Users, Teacher.user_id == Users.user_id)\
         .order_by(desc(LessonUpdates.created_at))\
         .limit(10).all()
        
        recent_lessons_data = [{
            'lesson': lesson.lesson,
            'subject': lesson.subject,
            'class': lesson.class_,
            'day': lesson.day,
            'created_at': lesson.created_at.isoformat(),
            'teacher': f"{lesson.first_name} {lesson.last_name}"
        } for lesson in recent_lessons]
        
        # Teacher-student connections
        teacher_connections = db.session.query(
            func.count(TeacherChild.id).label('total_connections')
        ).scalar()
        
        parent_connections = db.session.query(
            func.count(ParentChild.id).label('total_connections')
        ).scalar()
        
        # Average XP and streak
        avg_stats = db.session.query(
            func.avg(Child.xp_points).label('avg_xp'),
            func.avg(Child.streak).label('avg_streak'),
            func.max(Child.xp_points).label('max_xp'),
            func.max(Child.streak).label('max_streak')
        ).first()
        
        # Monthly growth trends (last 6 months)
        monthly_growth = []
        for i in range(6):
            month_start = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            
            new_students = Users.query.filter(
                and_(
                    Users.role_type == 'CHILD',
                    Users.created_at >= month_start,
                    Users.created_at < month_end
                )
            ).count()
            
            monthly_growth.append({
                'month': month_start.strftime('%Y-%m'),
                'new_students': new_students
            })
        
        # Completion rates
        habit_completion_rate = (total_habit_completions / max(total_habits, 1)) * 100
        skill_completion_rate = (total_skills_learned / max(total_skills, 1)) * 100
        todo_completion_rate = (total_todos_completed / max(total_todos, 1)) * 100
        
        # Build the comprehensive response
        overview_data = {
            'summary': {
                'total_users': total_users,
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_parents': total_parents,
                'total_schools': total_schools,
                'total_organizations': total_organizations,
                'active_students_30_days': active_students
            },
            'engagement_metrics': {
                'total_habits': total_habits,
                'total_habit_completions': total_habit_completions,
                'habit_completion_rate': round(habit_completion_rate, 2),
                'total_skills': total_skills,
                'total_skills_learned': total_skills_learned,
                'skill_completion_rate': round(skill_completion_rate, 2),
                'total_badges_earned': total_badges_earned,
                'total_todos': total_todos,
                'total_todos_completed': total_todos_completed,
                'todo_completion_rate': round(todo_completion_rate, 2),
                'total_gratitude_entries': total_gratitude_entries
            },
            'top_performers': {
                'students': top_students_data,
                'average_stats': {
                    'avg_xp': round(avg_stats.avg_xp or 0, 2),
                    'avg_streak': round(avg_stats.avg_streak or 0, 2),
                    'max_xp': avg_stats.max_xp or 0,
                    'max_streak': avg_stats.max_streak or 0
                }
            },
            'trends': {
                'habit_completions_7_days': habit_trends,
                'monthly_student_growth': monthly_growth
            },
            'popular_content': {
                'skills': popular_skills_data,
                'badges': badge_distribution,
                'habit_categories': habit_category_data
            },
            'demographics': {
                'class_distribution': class_data,
                'gender_distribution': gender_data
            },
            'connections': {
                'teacher_student_links': teacher_connections,
                'parent_child_links': parent_connections
            },
            'recent_activity': {
                'lessons': recent_lessons_data
            },
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return overview_data
        
    except Exception as e:
        return {'error': f'Failed to generate overview: {str(e)}'}


class OrganizationStats(Resource):
    @jwt_required()
    def get(self):
        """
        Get statistics for the organization.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.PRINCIPAL).first()

            if not user:
                return {'error': 'Unauthorized access'}, 403

            stats = get_overview_dashboard()
            return stats, 200

        except Exception as e:
            return {'error': f'Failed to retrieve organization stats: {str(e)}'}, 500  
