from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from api import jwt
from urls import api

app = Flask(__name__)
CORS(app)

app.config.from_object(config['default'])

api.init_app(app)
jwt.init_app(app)

db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == "__main__":
  app.run(host="", port=5000, debug=True)