from datetime import date, datetime, timedelta, timezone
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import func
from models import *
from utils import *



class AddStudent(Resource):
    @jwt_required()
    def post(self):
        """ 
        Add a student to a teacher's class by
        providing the student's email.
        """
        try:
            current_user_id = get_jwt_identity()
            teacher_user = Users.query.filter_by(user_id=current_user_id).first()
            
            if not teacher_user or teacher_user.role_type != UserRole.TEACHER:
                return {"message": "Unauthorized access"}, 401

            data = request.get_json()
            student_email = data.get("student_email")

            if not student_email:
                return {"message": "Student email is required"}, 400

            student_user = Users.query.filter_by(email=student_email).first()
            if not student_user:
                return {"message": "Student not found"}, 404

            student = Child.query.filter_by(user_id=student_user.user_id).first()
            if not student:
                return {"message": "Student not found"}, 404

            teacher = Teacher.query.filter_by(user_id=teacher_user.user_id).first()
            if not teacher:
                return {"message": "Teacher not found"}, 404

            existing_link = TeacherChild.query.filter_by(
                teacher_id=teacher.teacher_id, child_id=student.child_id
            ).first()
            if existing_link:
                return {"message": "Student already linked to this teacher"}, 400

            new_link = TeacherChild(
                teacher_id=teacher.teacher_id, child_id=student.child_id
            )
            db.session.add(new_link)
            db.session.commit()

            return {"message": "Student added successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class RemoveStudent(Resource):
    @jwt_required()
    def delete(self, student_id):
        """ 
        Remove a student from a teacher's class.
        """
        try:
            current_user_id = get_jwt_identity()
            teacher_user = Users.query.filter_by(user_id=current_user_id).first()
            
            if not teacher_user or teacher_user.role_type != UserRole.TEACHER:
                return {"message": "Unauthorized access"}, 401

            teacher = Teacher.query.filter_by(user_id=teacher_user.user_id).first()
            if not teacher:
                return {"message": "Teacher not found"}, 404

            link = TeacherChild.query.filter_by(
                teacher_id=teacher.teacher_id, child_id=student_id
            ).first()
            if not link:
                return {"message": "Student is not linked to this teacher"}, 404

            db.session.delete(link)
            db.session.commit()

            return {"message": "Student removed successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

