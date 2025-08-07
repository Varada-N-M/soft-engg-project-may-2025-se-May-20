def test_link_student_success(client, db, teacher_user, create_test_child, teacher_auth_header):
    user, child = create_test_child()
    response = client.post(
        "/api/teacher/link-student",  # Adjust path if needed
        json={"student_email": user.email},
        headers=teacher_auth_header
    )
    assert response.status_code == 201
    assert response.json["message"] == "Student linked successfully"
def test_link_student_already_linked(client, db, teacher_user, create_test_child, teacher_auth_header):
    user, child = create_test_child()
    from models import TeacherChild

    # Manually link before sending request
    _, teacher = teacher_user
    db.session.add(TeacherChild(teacher_id=teacher.teacher_id, child_id=child.child_id))
    db.session.commit()

    response = client.post(
        "/api/teacher/link-student",
        json={"student_email": user.email},
        headers=teacher_auth_header
    )
    assert response.status_code == 400
    assert response.json["error"] == "Student already linked to this teacher"

def test_link_student_missing_email(client, teacher_auth_header):
    response = client.post(
        "/api/teacher/link-student",
        json={},
        headers=teacher_auth_header
    )
    assert response.status_code == 400
    assert response.json["error"] == "Student email is required"
def test_link_student_not_found(client, teacher_auth_header):
    response = client.post(
        "/api/teacher/link-student",
        json={"student_email": "nonexistent@example.com"},
        headers=teacher_auth_header
    )
    assert response.status_code == 404
    assert response.json["error"] == "Student not found"
def test_unlink_student_success(client, db, teacher_user, create_test_child, teacher_auth_header):
    user, child = create_test_child()
    from models import TeacherChild
    _, teacher = teacher_user

    db.session.add(TeacherChild(teacher_id=teacher.teacher_id, child_id=child.child_id))
    db.session.commit()

    response = client.delete(
        f"/api/teacher/unlink-student/{child.child_id}",
        headers=teacher_auth_header
    )
    assert response.status_code == 200
    assert response.json["message"] == "Student unlinked successfully"
def test_unlink_student_not_linked(client, create_test_child, teacher_auth_header):
    user, child = create_test_child()

    response = client.delete(
        f"/api/teacher/unlink-student/{child.child_id}",
        headers=teacher_auth_header
    )
    assert response.status_code == 404
    assert response.json["error"] == "Student is not linked to this teacher"
