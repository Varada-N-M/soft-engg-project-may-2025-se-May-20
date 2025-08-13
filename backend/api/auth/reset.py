from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from config import config


mail = Mail()

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

def send_reset_email(user):
    """
    Send a password reset email to the user.
    """
    token = generate_reset_token(user.email)
    reset_url = f"{FRONTEND_URL}/user/password/change?token={token}"
    try:
        msg = Message("Reset Your Password", recipients=[user.email])
        msg.body = f"Click to reset your password: {reset_url}"
        msg.html = f'<p>Click to reset your password: <a href="{reset_url}">Reset Password</a></p>'
        mail.send(msg)
    except Exception as e:
        print(f"Error sending reset email: {e}")