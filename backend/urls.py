from flask_restful import Api
from api.auth.routes import SignupChild, Login, RefreshToken, SignupParent, SignupOrganization
from api.student.routes import GratitudeEntry, Habits
from api.parent.routes import LinkChildToParent
from api.student.routes import SkillResource, CompleteSkillResource, SkillStatsResource, SkillSearchResource

api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(RefreshToken, '/api/refresh-token')
api.add_resource(SignupChild, '/api/child/register')
api.add_resource(SignupParent, '/api/parent/register')
api.add_resource(SignupOrganization, '/api/organization/register')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')
api.add_resource(Habits, '/api/child/habit', '/api/child/habit/<int:habit_id>', '/api/child/habit/<int:habit_id>/complete')


# Parent
api.add_resource(LinkChildToParent, '/api/parent/link-child', '/api/parent/unlink-child/<int:child_id>')


# Register the resources with their URL patterns
api.add_resource(SkillResource, '/skills', '/skills/<int:skill_id>')
api.add_resource(CompleteSkillResource, '/skills/<int:skill_id>/complete')
api.add_resource(SkillStatsResource, '/skills/stats')
api.add_resource(SkillSearchResource, '/skills/search')