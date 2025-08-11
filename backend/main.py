from flask import Flask, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from api.auth import jwt
from config import config
from models import db
from urls import api


def create_app(config_name='default', testing=False):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    if testing:
        app.config['TESTING'] = True

    # Setup CORS - Allow frontend origins to access backend
    CORS(app, 
         origins=['http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:3000', 'http://localhost:5174'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With', 'Access-Control-Allow-Origin'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    Migrate(app, db)

    # Create tables on startup (optional)
    with app.app_context():
        db.create_all()

    # Swagger redirection
    @app.route('/')
    def index():
        return redirect('/static/swagger.html')
    return app

  

