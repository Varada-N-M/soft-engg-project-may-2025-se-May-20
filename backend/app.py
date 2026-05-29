from flask import Flask, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from api.auth import jwt
from config import config
from models import db
from urls import api
from api.auth.reset import mail

def create_app(config_name='default', testing=False):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    if testing:
        app.config['TESTING'] = True

    # Setup CORS - Allow specific frontend origins
    allowed_origins = [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:3000',
        'http://localhost:5174',
        'https://growwise-o79a.onrender.com',  # Production frontend
        config[config_name].FRONTEND_URL,  # Load from config
    ]
    CORS(app, 
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    # Create tables on startup (wrapped in try-except to prevent crash)
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not create database tables on startup: {str(e)}")
            print("⚠️ The app will still run, but database may not be initialized.")
            print("⚠️ Tables will be created when database becomes available.")

    # Swagger redirection
    @app.route('/')
    def index():
        return redirect('/static/swagger.html')
    return app

  

