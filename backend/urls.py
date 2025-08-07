from flask_restful import Api
from api.auth.routes import SignupChild, Login, RefreshToken, SignupParent, SignupOrganization, SignupTeacher, SignupAdmin
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, ToDoListResource, StudentLessonUpdates
from api.parent.routes import LinkChildToParent
from api.student.routes import Skills
from api.teacher.routes import AddStudent, RemoveStudent, TeacherLessonUpdates, TeacherLessonUpdateDetail, CreateSchool
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

# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')

# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')
api.add_resource(TeacherLessonUpdates, '/api/teacher/lesson-updates')
api.add_resource(TeacherLessonUpdateDetail, '/api/teacher/lesson-updates/<int:lesson_id>')

# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
