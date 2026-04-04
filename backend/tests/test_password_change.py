import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from models import Users, UserRole
from backend.app import db

# ---------------------------
# Forgot Password Tests
# ---------------------------
def test_forgot_password_valid_email(client, create_test_user, monkeypatch):
    """Test forgot password with valid email triggers email sending."""
    user = create_test_user(role=UserRole.CHILD, email="child@example.com")

    called = {}

    # Replace send_reset_email with a fake function
    def fake_send_reset_email(u):
        called["user"] = u

    monkeypatch.setattr("api.auth.routes.send_reset_email", fake_send_reset_email)

    response = client.post("/api/auth/forgot-password", json={"email": user.email})

    print(f"Forgot password test - Status: {response.status_code}")
    print(f"Forgot password test - Data: {response.get_data(as_text=True)}")

    assert response.status_code == 200
    assert "reset link has been sent" in response.get_json()["message"].lower()
    assert called["user"] == user


def test_forgot_password_invalid_email(client):
    """Test forgot password with non-existing email still returns 200."""
    response = client.post("/api/auth/forgot-password", json={"email": "notfound@example.com"})
    assert response.status_code == 200
    assert "reset link has been sent" in response.get_json()["message"].lower()


def test_forgot_password_missing_email(client):
    """Test forgot password with missing email returns 400."""
    response = client.post("/api/auth/forgot-password", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email is required"


# ---------------------------
# Reset Password Tests
# ---------------------------
def test_reset_password_valid_token(client, create_test_user, monkeypatch):
    """Test reset password with valid token updates password."""
    user = create_test_user(role=UserRole.CHILD, email="child@example.com")

    # Monkeypatch confirm_reset_token to return the user's email
    monkeypatch.setattr("api.auth.routes.confirm_reset_token", lambda token: user.email)

    response = client.post(
        "/api/auth/reset-password?token=validtoken",
        json={"new_password": "newsecurepass123"}
    )

    print(f"Reset password valid token - Status: {response.status_code}")
    print(f"Reset password valid token - Data: {response.get_data(as_text=True)}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Password reset successfully"

    # Verify password hash is updated
    db.session.refresh(user)
    assert user.password != "newsecurepass123"  # should be hashed


def test_reset_password_invalid_token(client, monkeypatch):
    """Test reset password with invalid token returns 400."""

    # Monkeypatch confirm_reset_token to always return None
    monkeypatch.setattr("api.auth.routes.confirm_reset_token", lambda token: None)

    response = client.post(
        "/api/auth/reset-password?token=badtoken",
        json={"new_password": "newpass"}
    )

    print(f"Reset password invalid token - Status: {response.status_code}")
    print(f"Reset password invalid token - Data: {response.get_data(as_text=True)}")

    assert response.status_code == 400
    assert "Invalid or expired token" in response.get_json()["error"]

def test_reset_password_missing_fields(client):
    """Test reset password missing token or new password returns 400."""
    response = client.post("/api/auth/reset-password", json={})
    assert response.status_code == 400
    assert "required" in response.get_json()["error"].lower()


# ---------------------------
# Change Password Tests
# ---------------------------
def test_change_password_success(client, create_test_user):
    """Test change password with valid old password works."""
    old_password = "oldpass123"
    user = create_test_user(
        role=UserRole.CHILD,
        email="child@example.com",
        password=generate_password_hash(old_password)
    )

    token = create_access_token(identity=str(user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/auth/change-password",
        json={"old_password": old_password, "new_password": "newpass456"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Password changed successfully"


def test_change_password_wrong_old_password(client, create_test_user):
    """Test change password with wrong old password fails."""
    user = create_test_user(
        role=UserRole.CHILD,
        email="child@example.com",
        password=generate_password_hash("correctpass")
    )

    token = create_access_token(identity=str(user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/auth/change-password",
        json={"old_password": "wrongpass", "new_password": "newpass456"},
        headers=headers
    )

    assert response.status_code == 400
    assert "Invalid current password" in response.get_json()["message"]


def test_change_password_missing_fields(client, create_test_user):
    """Test change password with missing fields returns 400."""
    user = create_test_user(role=UserRole.CHILD, email="child@example.com", password="test")
    token = create_access_token(identity=str(user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/auth/change-password", json={}, headers=headers)
    assert response.status_code == 400
    assert "required" in response.get_json()["error"].lower()
