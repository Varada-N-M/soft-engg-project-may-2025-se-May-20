import re
import random
import string
from models import db


# --- Utility functions --- #
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def generate_unique_key(model, field='unique_key', length=4):
    """Generates a unique key like AD81-652W for a given model and field."""
    characters = string.ascii_uppercase + string.digits

    while True:
        part1 = ''.join(random.choices(characters, k=length))
        part2 = ''.join(random.choices(characters, k=length))
        unique_key = f"{part1}-{part2}"

        # Check uniqueness in the database
        existing = db.session.query(model).filter(getattr(model, field) == unique_key).first()
        if not existing:
            return unique_key
        
