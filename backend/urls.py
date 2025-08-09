from flask_restful import Api
from api.auth.routes import SignupChild, Login, RefreshToken, SignupParent, SignupOrganization, SignupTeacher, SignupAdmin
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, ToDoListResource, StudentLessonUpdates, CompleteSkill,Skills,StudentProfile
from api.parent.routes import LinkChildToParent,ParentProfile
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, ToDoListResource, StudentLessonUpdates, CompleteSkill
from api.parent.routes import LinkChildToParent, GetLinkedChildren
from api.student.routes import Skills
from api.teacher.routes import (AddStudent, RemoveStudent, TeacherLessonUpdates, TeacherLessonUpdateDetail, CreateSchool, 
                                LinkStudentToTeacher, UnlinkStudentFromTeacher,TeacherProfile, GetLinkedStudents)
from api.organization.routes import OrganizationStats
from api.auth.routes import ForgotPassword, ResetPassword, ChangePassword

api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(RefreshToken, '/api/refresh-token')
api.add_resource(SignupChild, '/api/child/register')
api.add_resource(SignupParent, '/api/parent/register')
api.add_resource(SignupOrganization, '/api/organization/register')
api.add_resource(SignupTeacher, '/api/teacher/register')
api.add_resource(SignupAdmin, '/api/admin/register')

api.add_resource(CreateSchool, '/api/admin/add-school')

api.add_resource(ForgotPassword, '/api/auth/forgot-password')
api.add_resource(ResetPassword, '/api/auth/reset-password')
api.add_resource(ChangePassword, '/api/auth/change-password')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')
api.add_resource(Habits, '/api/child/habit', '/api/child/habit/<int:habit_id>')
api.add_resource(CompleteHabit, '/api/child/habit/<int:habit_id>/complete')
api.add_resource(ToDoListResource, '/api/todos', '/api/todos/<int:todo_id>')
api.add_resource(StudentLessonUpdates, '/api/child/lesson-updates')
api.add_resource(Skills, '/api/child/skills', '/api/child/skills/<int:skill_id>')
api.add_resource(CompleteSkill, '/api/child/skills/<int:skill_id>/complete')
api.add_resource(StudentProfile, '/api/child/profile')

# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')
api.add_resource(ParentProfile, '/api/parent/profile')
api.add_resource(GetLinkedChildren, '/api/parent/linked-children')

# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')
api.add_resource(TeacherLessonUpdates, '/api/teacher/lesson-updates')
api.add_resource(TeacherLessonUpdateDetail, '/api/teacher/lesson-updates/<int:lesson_id>')
api.add_resource(LinkStudentToTeacher, '/api/teacher/link-student')
api.add_resource(UnlinkStudentFromTeacher, '/api/teacher/unlink-student/<int:student_id>')
api.add_resource(TeacherProfile, '/api/teacher/profile')
api.add_resource(GetLinkedStudents, '/api/teacher/linked-students')
# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
