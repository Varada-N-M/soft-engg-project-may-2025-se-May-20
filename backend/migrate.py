from models import db
from config import Config
from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if os.path.exists(db_path):
        confirm = input("WARNING: This will DELETE and RECREATE the database. Type 'yes' to continue: ")
        if confirm.lower() == 'yes':
            os.remove(db_path)
            print("Old database removed.")
        else:
            print("Migration cancelled.")
            exit(0)
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('Database tables created successfully!')
