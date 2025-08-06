from flask_restful import Api

from api.auth.routes import (ChangePassword, ForgotPassword, Login,
                             RefreshToken, ResetPassword, SignupChild,
                             SignupOrganization, SignupParent, SignupTeacher)
from api.organization.routes import OrganizationStats
from api.parent.routes import LinkChildToParent
from api.student.routes import (CompleteHabit, CompleteSkillResource,
                                GratitudeEntry, Habits, SkillResource,
                                SkillSearchResource, SkillStatsResource,
                                ToDoListResource)
from api.teacher.routes import AddStudent, RemoveStudent

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
api.add_resource(SkillResource, '/api/skills', '/api/skills/<int:skill_id>')
api.add_resource(CompleteSkillResource, '/api/skills/<int:skill_id>/complete')
api.add_resource(SkillStatsResource, '/api/skills/stats')
api.add_resource(SkillSearchResource, '/api/skills/search')
# Teacher
api.add_resource(AddStudent, '/api/teacher/add-student')
api.add_resource(RemoveStudent, '/api/teacher/remove-student/<int:student_id>')

# Organization
api.add_resource(OrganizationStats, '/api/organization/stats')
