from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)