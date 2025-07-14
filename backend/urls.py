from api import *
from flask_restful import Api

api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(RefreshToken, '/api/refresh-token')
api.add_resource(SignupChild, '/api/child/register')
api.add_resource(SignupParent, '/api/parent/register')
api.add_resource(SignupOrganization, '/api/organization/register')

# Student
api.add_resource(GratitudeEntry, '/api/child/gratitude', '/api/child/gratitude/<int:entry_id>')

