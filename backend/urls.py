from flask_restful import Api
from api.auth.routes import SignupChild, Login, RefreshToken, SignupParent, SignupOrganization, SignupTeacher
from api.student.routes import GratitudeEntry, Habits, CompleteHabit, ToDoListResource
from api.parent.routes import LinkChildToParent
from api.student.routes import SkillResource, CompleteSkillResource, SkillStatsResource, SkillSearchResource
from api.teacher.routes import AddStudent, RemoveStudent
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

api.add_resource(ForgotPassword, '/api/auth/forgot-password')
api.add_resource(ResetPassword, '/api/auth/reset-password')
api.add_resource(ChangePassword, '/api/auth/change-password')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')
api.add_resource(Habits, '/api/child/habit', '/api/child/habit/<int:habit_id>')
api.add_resource(CompleteHabit, '/api/child/habit/<int:habit_id>/complete')
api.add_resource(ToDoListResource, '/api/todos', '/api/todos/<int:todo_id>')

# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')


# Register the resources with their URL patterns
api.add_resource(SkillResource, '/skills', '/skills/<int:skill_id>')
api.add_resource(CompleteSkillResource, '/skills/<int:skill_id>/complete')
api.add_resource(SkillStatsResource, '/skills/stats')
api.add_resource(SkillSearchResource, '/skills/search')
# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')

# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
