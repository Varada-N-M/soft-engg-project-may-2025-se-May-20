from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from models import *
from sqlalchemy import func

class OrganizationStats(Resource):
    @jwt_required()
    def get(self):
        """
        Get statistics for the organization.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id).first()

            if not user or user.role_type != UserRole.ORGANIZATION:
                return {"message": "Unauthorized access"}, 401

            organization = Organization.query.filter_by(created_by=user.user_id).first()
            if not organization:
                return {"message": "Organization not found"}, 404

            # Get all schools created by the organization's creator
            schools = School.query.filter_by(created_by=user.user_id).all()
            school_ids = [school.school_id for school in schools]

            # Get all teachers in those schools
            teachers = Teacher.query.filter(Teacher.school_id.in_(school_ids)).all()
            teacher_ids = [teacher.teacher_id for teacher in teachers]

            # Get all students linked to those teachers
            student_links = TeacherChild.query.filter(TeacherChild.teacher_id.in_(teacher_ids)).all()
            student_ids = [link.child_id for link in student_links]

            # Get all students
            students = Child.query.filter(Child.child_id.in_(student_ids)).all()

            # Anonymized student data
            anonymized_students = []
            for student in students:
                anonymized_students.append({
                    "student_id": student.child_id,
                    "xp_points": student.xp_points,
                    "streak": student.streak,
                    "habits_completed": HabitCompletion.query.filter_by(child_id=student.child_id, is_done=True).count(),
                    "badges_earned": Badge.query.filter_by(child_id=student.child_id, is_earned=True).count(),
                    "skills_learned": Skill.query.filter_by(child_id=student.child_id, is_learned=True).count(),
                })

            # School performance
            school_performance = []
            for school in schools:
                school_teachers = Teacher.query.filter_by(school_id=school.school_id).all()
                school_teacher_ids = [teacher.teacher_id for teacher in school_teachers]
                school_student_links = TeacherChild.query.filter(TeacherChild.teacher_id.in_(school_teacher_ids)).all()
                school_student_ids = [link.child_id for link in school_student_links]
                school_students = Child.query.filter(Child.child_id.in_(school_student_ids)).all()

                total_xp = 0
                for student in school_students:
                    total_xp += student.xp_points

                school_performance.append({
                    "school_id": school.school_id,
                    "school_name": school.name,
                    "number_of_students": len(school_students),
                    "average_xp_per_student": total_xp / len(school_students) if school_students else 0,
                })

            return {
                "anonymized_student_data": anonymized_students,
                "school_performance": school_performance,
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
