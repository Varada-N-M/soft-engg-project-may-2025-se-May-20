from flask_restful import Api
from api import *

api = Api()

# Login
api.add_resource(Login, '/api/login')
api.add_resource(Signup, '/api/register')
api.add_resource(RefreshToken, '/api/refresh-token')
