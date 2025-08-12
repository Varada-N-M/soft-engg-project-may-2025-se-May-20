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

class TeacherLessonUpdates(Resource):
    @jwt_required()
    def get(self):
        """
        Get all lesson updates for the logged-in teacher user.
        Returns lesson updates created by this teacher.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can view lesson updates'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            lesson_updates = LessonUpdates.query.filter_by(teacher_id=teacher.teacher_id).order_by(LessonUpdates.created_at.desc()).all()

            result = []
            for lesson in lesson_updates:
                result.append({
                    'id': lesson.id,
                    'day': lesson.day,
                    'subject': lesson.subject,
                    'lesson': lesson.lesson,
                    'activity': lesson.activity,
                    'class': lesson.class_,
                    'created_at': lesson.created_at.isoformat(),
                })

            return {'lessons': result}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def post(self):
        """
        Create a new lesson update for the logged-in teacher.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can create lesson updates'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            data = request.get_json()
            
            # Validate required fields
            required_fields = ['day', 'subject', 'lesson', 'activity', 'class_']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            # Validate day
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            if data['day'] not in valid_days:
                return {'error': 'Invalid day. Must be one of: Monday, Tuesday, Wednesday, Thursday, Friday'}, 400

            # Validate subject
            valid_subjects = ['Math', 'English', 'Science', 'Social Studies', 'Computers']
            if data['subject'] not in valid_subjects:
                return {'error': 'Invalid subject. Must be one of: Math, English, Science, Social Studies, Computers'}, 400

            # Validate class
            class_level = data.get('class_')
            if not isinstance(class_level, int) or class_level < 1 or class_level > 12:
                return {'error': 'Invalid class level. Must be an integer between 1 and 12'}, 400

            # Create new lesson update
            new_lesson = LessonUpdates(
                teacher_id=teacher.teacher_id,
                class_=data['class_'],
                day=data['day'],
                subject=data['subject'],
                lesson=data['lesson'],
                activity=data['activity']
            )

            db.session.add(new_lesson)
            db.session.commit()

            return {
                'message': 'Lesson update created successfully',
                'lesson': {
                    'id': new_lesson.id,
                    'day': new_lesson.day,
                    'subject': new_lesson.subject,
                    'lesson': new_lesson.lesson,
                    'activity': new_lesson.activity,
                    'class': new_lesson.class_,
                    'created_at': new_lesson.created_at.isoformat(),
                }
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class TeacherLessonUpdateDetail(Resource):
    @jwt_required()
    def get(self, lesson_id):
        """
        Get a specific lesson update by ID.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can view lesson updates'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            lesson = LessonUpdates.query.filter_by(id=lesson_id, teacher_id=teacher.teacher_id).first()
            if not lesson:
                return {'error': 'Lesson update not found'}, 404

            return {
                'id': lesson.id,
                'day': lesson.day,
                'subject': lesson.subject,
                'lesson': lesson.lesson,
                'activity': lesson.activity,
                'class': lesson.class_,
                'created_at': lesson.created_at.isoformat(),
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def put(self, lesson_id):
        """
        Update a specific lesson update by ID.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can update lesson updates'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            lesson = LessonUpdates.query.filter_by(id=lesson_id, teacher_id=teacher.teacher_id).first()
            if not lesson:
                return {'error': 'Lesson update not found'}, 404

            data = request.get_json()
            
            # Validate required fields
            required_fields = ['day', 'subject', 'lesson', 'activity', 'class_']
            for field in required_fields:
                if not data.get(field):
                    return {'error': f'{field} is required'}, 400

            # Validate day
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            if data['day'] not in valid_days:
                return {'error': 'Invalid day. Must be one of: Monday, Tuesday, Wednesday, Thursday, Friday'}, 400

            # Validate subject
            valid_subjects = ['Math', 'English', 'Science', 'Social Studies', 'Computers']
            if data['subject'] not in valid_subjects:
                return {'error': 'Invalid subject. Must be one of: Math, English, Science, Social Studies, Computers'}, 400

            # Validate class
            class_level = data.get('class_')
            if not isinstance(class_level, int) or class_level < 1 or class_level > 12:
                return {'error': 'Invalid class level. Must be an integer between 1 and 12'}, 400

            # Update lesson
            lesson.day = data['day']
            lesson.subject = data['subject']
            lesson.lesson = data['lesson']
            lesson.activity = data['activity']
            lesson.class_ = data['class_']

            db.session.commit()

            return {
                'message': 'Lesson update updated successfully',
                'lesson': {
                    'id': lesson.id,
                    'day': lesson.day,
                    'subject': lesson.subject,
                    'lesson': lesson.lesson,
                    'activity': lesson.activity,
                    'class': lesson.class_,
                    'created_at': lesson.created_at.isoformat(),
                }
            }, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

    @jwt_required()
    def delete(self, lesson_id):
        """
        Delete a specific lesson update by ID.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can delete lesson updates'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            lesson = LessonUpdates.query.filter_by(id=lesson_id, teacher_id=teacher.teacher_id).first()
            if not lesson:
                return {'error': 'Lesson update not found'}, 404

            db.session.delete(lesson)
            db.session.commit()

            return {'message': 'Lesson update deleted successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class CreateSchool(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new school. Only accessible by principal.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.PRINCIPAL).first()

            if not user:
                return {'error': 'Only principal user can create schools'}, 403

            data = request.get_json()
            name = data.get('name')
            phone_number = data.get('phone_number')
            address = data.get('address')

            if not name or not phone_number or not address:
                return {'error': 'Name, phone number, and address are required'}, 400

            new_school = School(
                name=name,
                phone_number=phone_number,
                address=address,
                created_by=current_user_id
            )

            db.session.add(new_school)
            db.session.commit()

            return {'message': 'School created successfully', 'school_id': new_school.school_id}, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class LinkStudentToTeacher(Resource):
    @jwt_required()
    def post(self):
        """
        Link a student to a teacher using the student's email.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can link students'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            data = request.get_json()
            student_email = data.get('student_email')

            if not student_email:
                return {'error': 'Student email is required'}, 400

            student_user = Users.query.filter_by(email=student_email).first()
            if not student_user:
                return {'error': 'Student not found'}, 404

            student = Child.query.filter_by(user_id=student_user.user_id).first()
            if not student:
                return {'error': 'Student profile not found'}, 404

            existing_link = TeacherChild.query.filter_by(
                teacher_id=teacher.teacher_id, child_id=student.child_id
            ).first()
            if existing_link:
                return {'error': 'Student already linked to this teacher'}, 400

            new_link = TeacherChild(
                teacher_id=teacher.teacher_id, child_id=student.child_id
            )
            db.session.add(new_link)
            db.session.commit()

            return {'message': 'Student linked successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500


class UnlinkStudentFromTeacher(Resource):
    @jwt_required()
    def delete(self, student_id):
        """
        Unlink a student from a teacher.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can unlink students'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            link = TeacherChild.query.filter_by(
                teacher_id=teacher.teacher_id, child_id=student_id
            ).first()
            if not link:
                return {'error': 'Student is not linked to this teacher'}, 404

            db.session.delete(link)
            db.session.commit()

            return {'message': 'Student unlinked successfully'}, 200

        except Exception as e:
            db.session.rollback()
            return {'error': 'Internal server error', 'details': str(e)}, 500

class TeacherProfile(Resource):
    @jwt_required()
    def get(self):
        """
        Get the profile of the logged-in teacher user.
        Returns basic information about the teacher user.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can view their profile'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            return {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'school_id': teacher.school_id,
                'teacher_id': teacher.teacher_id,
                'subject': teacher.subject,
                'created_at': user.created_at.isoformat(),
            }, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500


class GetLinkedStudents(Resource):
    @jwt_required()
    def get(self):
        """
        Get all students linked to the logged-in teacher.
        Returns a list of students linked to this teacher.
        """
        try:
            current_user_id = get_jwt_identity()
            user = Users.query.filter_by(user_id=current_user_id, is_active=True, role_type=UserRole.TEACHER).first()

            if not user:
                return {'error': 'Only active teacher users can view linked students'}, 403

            teacher = Teacher.query.filter_by(user_id=user.user_id).first()
            if not teacher:
                return {'error': 'Teacher profile not found'}, 404

            links = TeacherChild.query.filter_by(teacher_id=teacher.teacher_id).all()
            students = []
            for link in links:
                student = Child.query.get(link.child_id)
                if student:
                    students.append({
                        'student_id': student.child_id,
                        'first_name': student.user.first_name,
                        'last_name': student.user.last_name,
                        'email': student.user.email,
                    })

            return {'students': students}, 200

        except Exception as e:
            return {'error': 'Internal server error', 'details': str(e)}, 500
  

class PrincipalTeacher(Resource):
    """
    GET /principal/teachers -> list all teachers in principal's school (except themselves)
    """

    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            principal_user = Users.query.filter_by(user_id=current_user_id).first()

            if not principal_user or principal_user.role_type != UserRole.PRINCIPAL:
                return {"message": "Unauthorized access"}, 401

            # Get principal's school_id from Teacher table
            principal_teacher_entry = Teacher.query.filter_by(user_id=principal_user.user_id).first()
            if not principal_teacher_entry:
                return {"message": "Principal is not linked to any school"}, 404

            school = School.query.filter_by(school_id=principal_teacher_entry.school_id).first()
            if not school:
                return {"message": "School not found"}, 404

            # List all teachers in school except principal themselves
            teachers = Teacher.query.filter(
                Teacher.school_id == school.school_id,
                Teacher.user_id != principal_user.user_id
            ).all()

            teacher_list = []
            for t in teachers:
                u = t.user
                teacher_list.append({
                    "teacher_id": t.teacher_id,
                    "user_id": t.user_id,
                    "first_name": u.first_name if u else None,
                    "last_name": u.last_name if u else None,
                    "email": u.email if u else None,
                    "subject": t.subject,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                })

            return {
                "school_id": school.school_id,
                "school_name": school.name,
                "teachers": teacher_list
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500


class PrincipalTeacherManagement(Resource):
    """
    GET /principal/teachers/<id> -> get single teacher (if in school)
    DELETE /principal/teachers/<id> -> remove teacher (not themselves)
    """

    @jwt_required()
    def get(self, teacher_id):
        try:
            current_user_id = get_jwt_identity()
            principal_user = Users.query.filter_by(user_id=current_user_id).first()

            if not principal_user or principal_user.role_type != UserRole.PRINCIPAL:
                return {"message": "Unauthorized access"}, 401

            principal_teacher_entry = Teacher.query.filter_by(user_id=principal_user.user_id).first()
            if not principal_teacher_entry:
                return {"message": "Principal is not linked to any school"}, 404

            school = School.query.filter_by(school_id=principal_teacher_entry.school_id).first()
            if not school:
                return {"message": "School not found"}, 404

            teacher = Teacher.query.filter_by(
                teacher_id=teacher_id, school_id=school.school_id
            ).first()

            if not teacher or teacher.user_id == principal_user.user_id:
                return {"message": "Teacher not found in your school"}, 404

            user = teacher.user
            return {
                "teacher_id": teacher.teacher_id,
                "user_id": teacher.user_id,
                "first_name": user.first_name if user else None,
                "last_name": user.last_name if user else None,
                "email": user.email if user else None,
                "subject": teacher.subject,
                "created_at": teacher.created_at.isoformat() if teacher.created_at else None
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()
    def delete(self, teacher_id):
        try:
            current_user_id = get_jwt_identity()
            principal_user = Users.query.filter_by(user_id=current_user_id).first()

            if not principal_user or principal_user.role_type != UserRole.PRINCIPAL:
                return {"message": "Unauthorized access"}, 401

            principal_teacher_entry = Teacher.query.filter_by(user_id=principal_user.user_id).first()
            if not principal_teacher_entry:
                return {"message": "Principal is not linked to any school"}, 404

            school = School.query.filter_by(school_id=principal_teacher_entry.school_id).first()
            if not school:
                return {"message": "School not found"}, 404

            teacher = Teacher.query.filter_by(
                teacher_id=teacher_id, school_id=school.school_id
            ).first()

            if not teacher or teacher.user_id == principal_user.user_id:
                return {"message": "Teacher not found in your school"}, 404

            user = Users.query.get(teacher.user_id)
            db.session.delete(teacher)
            if user:
                db.session.delete(user)

            db.session.commit()
            return {"message": "Teacher removed successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class GetSchools(Resource):
    def get(self):
        """
        Get all available schools for registration.
        Public endpoint - no authentication required.
        """
        try:
            schools = School.query.all()
            schools_list = []
            for school in schools:
                schools_list.append({
                    "school_id": school.school_id,
                    "name": school.name,
                    "address": school.address,
                    "phone_number": school.phone_number
                })

            return {"schools": schools_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500
