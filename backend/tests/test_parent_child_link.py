import pytest
from flask_jwt_extended import create_access_token
from datetime import datetime
from backend.app import db
from models import Parent, Child, ParentChild, UserRole


# ---------------------------
# Link Child to Parent Tests
# ---------------------------
def test_link_child_success(client, create_test_user, child_user):
    """Link a child to a parent successfully."""
    parent_user = create_test_user(role=UserRole.PARENT, email="parent@example.com")
    _,child = child_user

    parent = Parent(user_id=parent_user.user_id)
    db.session.add(parent)
    db.session.commit()

    token = create_access_token(identity=str(parent_user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    print(child)
    response = client.post(
        "/api/parent/link-child",
        json={"child_key": child.unique_key},
        headers=headers,
    )

    print(response.get_json())
    assert response.status_code == 201
    assert "linked successfully" in response.get_json()["message"]

    # Verify database state
    link = ParentChild.query.filter_by(parent_id=parent.parent_id, child_id=child.child_id).first()
    assert link is not None
    assert child.is_linked is True


def test_link_child_missing_key(client, create_test_user):
    """Fail when child_key is missing."""
    parent_user = create_test_user(role=UserRole.PARENT, email="parent@example.com")
    parent = Parent(user_id=parent_user.user_id)
    db.session.add(parent)
    db.session.commit()

    token = create_access_token(identity=str(parent_user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/parent/link-child",
        json={},
        headers=headers,
    )

    assert response.status_code == 400
    assert "Child key is required" in response.get_json()["message"]


def test_link_child_not_found(client, create_test_user):
    """Fail when child is not found."""
    parent_user = create_test_user(role=UserRole.PARENT, email="parent@example.com")
    parent = Parent(user_id=parent_user.user_id)
    db.session.add(parent)
    db.session.commit()

    token = create_access_token(identity=str(parent_user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/parent/link-child",
        json={"child_key": "nonexistent"},
        headers=headers,
    )

    assert response.status_code == 404
    assert "Child not found" in response.get_json()["message"]


def test_link_child_already_linked_same_parent(client, create_test_user, child_user):
    """Fail when child is already linked to same parent."""
    parent_user = create_test_user(role=UserRole.PARENT, email="parent@example.com")
    _,child = child_user

    parent = Parent(user_id=parent_user.user_id)
    db.session.add(parent)
    db.session.commit()

    # Create existing link
    link = ParentChild(parent_id=parent.parent_id, child_id=child.child_id, linked_at=datetime.utcnow())
    db.session.add(link)
    child.is_linked = True
    db.session.commit()

    token = create_access_token(identity=str(parent_user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/parent/link-child",
        json={"child_key": child.unique_key},
        headers=headers,
    )

    assert response.status_code == 400
    assert "already linked to your account" in response.get_json()["message"]


def test_link_child_already_linked_other_parent(client, create_test_user, child_user):
    """Fail when child is already linked to another parent."""
    parent_user1 = create_test_user(role=UserRole.PARENT, email="parent1@example.com")
    parent1 = Parent(user_id=parent_user1.user_id)
    db.session.add(parent1)

    parent_user2 = create_test_user(role=UserRole.PARENT, email="parent2@example.com")
    parent2 = Parent(user_id=parent_user2.user_id)
    db.session.add(parent2)

    _,child = child_user
    db.session.commit()

    # Link child to parent1
    link = ParentChild(parent_id=parent1.parent_id, child_id=child.child_id, linked_at=datetime.utcnow())
    db.session.add(link)
    child.is_linked = True
    db.session.commit()

    token = create_access_token(identity=str(parent_user2.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/parent/link-child",
        json={"child_key": child.unique_key},
        headers=headers,
    )

    assert response.status_code == 400
    assert "already linked to another parent" in response.get_json()["message"]


# ---------------------------
# Unlink Child from Parent Tests
# ---------------------------
def test_unlink_child_success(client, create_test_user, child_user):
    """Unlink a child from a parent successfully."""
    parent_user = create_test_user(role=UserRole.PARENT, email="parent@example.com")
    parent = Parent(user_id=parent_user.user_id)
    db.session.add(parent)

    _,child = child_user
    db.session.commit()

    # Create link
    link = ParentChild(parent_id=parent.parent_id, child_id=child.child_id, linked_at=datetime.utcnow())
    db.session.add(link)
    child.is_linked = True
    db.session.commit()

    token = create_access_token(identity=str(parent_user.user_id))
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(
        f"/api/parent/unlink-child/{child.child_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert "unlinked successfully" in response.get_json()["message"]

    # Verify removal
    link_check = ParentChild.query.filter_by(parent_id=parent.parent_id, child_id=child.child_id).first()
    assert link_check is None
    db.session.refresh(child)
    assert child.is_linked is False



