import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'dev'

    FRONTEND_URL = os.environ.get("FRONTEND_URL") or 'https://growwise-o79a.onrender.com'

    # db config - Support both PostgreSQL and SQLite
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        # Use PostgreSQL if DATABASE_URL is provided
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to SQLite for local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_KEY") or 'dev'
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES") or timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = os.environ.get("JWT_REFRESH_TOKEN_EXPIRES") or timedelta(days=30)

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AIzaSyAQGw0FUUxJ4V3nS09DJIK_g1XAOlHY7F8"
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL") or "gemini-2.0-flash"

    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.gmail.com'
    MAIL_PORT = os.environ.get("MAIL_PORT") or 587
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or True
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") or False

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or 'hari.backup0007@gmail.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or 'zncn koyo ntek amjj'

    MAIL_DEFAULT_SENDER = ('GrowWise', 'hari.backup0007@gmail.com')


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}