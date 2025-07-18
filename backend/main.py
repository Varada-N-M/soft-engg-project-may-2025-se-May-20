from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from api.auth import jwt
from urls import api
from flask_migrate import Migrate

app = Flask(__name__)
# Add frontend URLs here
CORS(app, origins=['http://localhost:5173'])

app.config.from_object(config['default'])

api.init_app(app)
jwt.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == "__main__":
  app.run(host="", port=5000, debug=True)