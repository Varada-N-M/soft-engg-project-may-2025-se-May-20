from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from config import config

SECRET_KEY = config['default'].JWT_SECRET_KEY
FRONTEND_URL = config['default'].FRONTEND_URL

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt="password-reset")

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, salt="password-reset", max_age=expiration)
    except Exception:
        return None
    return email

### Need to implement email sending functionality ###
def send_reset_email(user):
    token = generate_reset_token(user.email)
    reset_url = f"{FRONTEND_URL}/api/auth/reset-password?token={token}"
    # msg = Message("Reset Your Password", recipients=[user.email])
    # msg.body = f"Click to reset your password: {reset_url}"
    print(f"Reset URL: {reset_url}")
    return reset_url