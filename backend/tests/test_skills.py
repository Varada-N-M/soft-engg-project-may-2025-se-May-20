from flask_jwt_extended import create_access_token


def test_create_skill_success(client, child_user, auth_header):
    user, child = child_user
    headers = auth_header

    payload = {
        "skill_name": "Ride a bike",
        "video_url": "https://video.example/ride",
        "skill_xp": 50
    }
    resp = client.post("/api/child/skills", json=payload, headers=headers)

    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["message"] == "Skill created successfully"
    skill = data["skill"]
    assert skill["skill_name"] == payload["skill_name"]
    assert skill["video_url"] == payload["video_url"]
    assert skill["skill_xp"] == payload["skill_xp"]
    assert skill["is_learned"] is False


def test_create_skill_missing_name_returns_400(client, child_user, auth_header):
    user, child = child_user
    headers = auth_header

    payload = {"skill_name": "   "}  # whitespace-only
    resp = client.post("/api/child/skills", json=payload, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Skill name is required" in (data.get("error") or "")


def test_get_skills_and_filtering(client, child_user,auth_header):
    user, child = child_user
    headers = auth_header

    # create two skills
    payload1 = {"skill_name": "A", "skill_xp": 10}
    payload2 = {"skill_name": "B", "skill_xp": 20, "is_learned": True}
    r1 = client.post("/api/child/skills", json=payload1, headers=headers)
    r2 = client.post("/api/child/skills", json=payload2, headers=headers)
    
    assert r1.status_code == 201
    assert r2.status_code == 201

    # get all
    resp_all = client.get("/api/child/skills", headers=headers)

    print(f"Response Status: {resp_all.status_code}")
    print(f"Response Data: {resp_all.get_json()}")
    assert resp_all.status_code == 200
    body_all = resp_all.get_json()
    assert body_all["total"] >= 2
    names = [s["skill_name"] for s in body_all["skills"]]
    assert "A" in names and "B" in names

    # filter is_learned=true
    resp_filtered = client.get("/api/child/skills?is_learned=true", headers=headers)
    
    print(f"Filtered Response Status: {resp_filtered.status_code}")
    print(f"Filtered Response Data: {resp_filtered.get_json()}")
    assert resp_filtered.status_code == 200
    body_f = resp_filtered.get_json()
    skills_filtered = body_f["skills"]
    assert all(s["is_learned"] for s in skills_filtered)


def test_update_skill_not_found_or_forbidden(client, child_user, auth_header):
    user, child = child_user
    headers = auth_header

    resp = client.put("/api/child/skills/999999", json={"skill_name": "X"}, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code in (404, 403)


def test_delete_skill_success(client, child_user, auth_header):
    user, child = child_user
    headers = auth_header

    create_resp = client.post("/api/child/skills", json={"skill_name": "DeleteMe"}, headers=headers)
    assert create_resp.status_code == 201
    skill = create_resp.get_json()["skill"]
    skill_id = skill.get("id") or skill.get("skill_id")

    del_resp = client.delete(f"/api/child/skills/{skill_id}", headers=headers)
    
    print(f"Response Status: {del_resp.status_code}")
    print(f"Response Data: {del_resp.get_json()}")
    assert del_resp.status_code == 200
    data = del_resp.get_json()
    assert "deleted_skill" in data or "deleted" in data.get("message", "").lower()

    # verify absent from list
    list_resp = client.get("/api/child/skills", headers=headers)
    assert list_resp.status_code == 200
    skills = list_resp.get_json()["skills"]
    ids = [s.get("id") or s.get("skill_id") for s in skills]
    assert skill_id not in ids


def test_unauthorized_access_returns_401(client):
    resp = client.post("/api/child/skills", json={"skill_name": "NoAuth"})
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code in (401, 422)


def test_complete_skill_success_and_awards_xp(client, child_user, auth_header):
    """
    Happy path: mark an unlearned skill as completed, add default XP (10),
    and expect at least one badge if conditions are met.
    """
    user, child = child_user
    headers = auth_header

    # Create a skill (not learned by default)
    create_resp = client.post(
        "/api/child/skills",
        json={"skill_name": "FinishMe", "skill_xp": 5},
        headers=headers
    )
    assert create_resp.status_code == 201
    skill = create_resp.get_json()["skill"]
    skill_id = skill.get("id") or skill.get("skill_id")

    # Call PATCH to complete the skill (no xp specified -> default 10)
    resp = client.patch(f"/api/child/skills/{skill_id}/complete", json={}, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code == 200, resp.get_data(as_text=True)

    data = resp.get_json()
    assert data["message"].startswith("Skill completed successfully")
    assert data["xp_earned"] == 10
    assert data["skill"]["is_learned"] is True
    assert "completion_date" in data["skill"]
    # At least returns a list for newly_earned_badges
    assert isinstance(data.get("newly_earned_badges", []), list)


def test_complete_skill_with_custom_xp(client, child_user, auth_header):
    """
    Provide custom XP to add in request body and ensure skill_xp updated correctly.
    """
    user, child = child_user
    headers = auth_header

    create_resp = client.post(
        "/api/child/skills",
        json={"skill_name": "XPTest", "skill_xp": 0},
        headers=headers
    )
    assert create_resp.status_code == 201
    skill = create_resp.get_json()["skill"]
    skill_id = skill.get("id") or skill.get("skill_id")

    resp = client.patch(f"/api/child/skills/{skill_id}/complete", json={"xp": 25}, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code == 200, resp.get_data(as_text=True)

    data = resp.get_json()
    assert data["xp_earned"] == 25
    assert data["skill"]["skill_xp"] >= 25


def test_complete_already_completed_skill_returns_400(client, child_user, auth_header):
    """
    If skill.is_learned is already True, return 400 with appropriate error.
    """
    user, child = child_user
    headers = auth_header

    # Create skill
    create_resp = client.post(
        "/api/child/skills",
        json={"skill_name": "Already"},
        headers=headers
    )
    assert create_resp.status_code == 201
    skill = create_resp.get_json()["skill"]
    skill_id = skill.get("id") or skill.get("skill_id")

    # Mark learned using PUT endpoint (server sets is_learned=True)
    put_resp = client.put(f"/api/child/skills/{skill_id}", json={"is_learned": True}, headers=headers)
    assert put_resp.status_code == 200

    # Try completing again → expect 400
    resp = client.patch(f"/api/child/skills/{skill_id}/complete", json={}, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code == 400, resp.get_data(as_text=True)
    assert "already" in (resp.get_json().get("error") or "").lower()

def test_complete_skill_not_found_or_forbidden(client, child_user, auth_header):
    """
    Completing a non-existent or other-child's skill should return 404 or 403.
    """
    user, child = child_user
    headers = auth_header

    resp = client.patch("/api/child/skills/999999/complete", json={}, headers=headers)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code in (403, 404)


def test_complete_skill_unauthorized_returns_401(client):
    """
    No auth header should return 401 (or 422 depending on JWT config).
    """
    resp = client.patch("/api/child/skills/1/complete", json={})
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code in (401, 422)


def test_child_cannot_complete_another_childs_skill(client, child_user, auth_header,create_test_child):
    """
    Ensure a child B cannot complete a skill belonging to child A.
    """
    user2, child = create_test_child()
    access_token2 = create_access_token(identity=str(user2.user_id))
    headers2 = {'Authorization': f'Bearer {access_token2}'}


    # user A creates a skill
    create_resp = client.post("/api/child/skills", json={"skill_name": "UserA Skill"}, headers=auth_header)
    assert create_resp.status_code == 201
    skill_id = create_resp.get_json()["skill"].get("id")

    # user B tries to complete it
    resp = client.patch(f"/api/child/skills/{skill_id}/complete", json={}, headers=headers2)
    
    print(f"Response Status: {resp.status_code}")
    print(f"Response Data: {resp.get_json()}")
    assert resp.status_code in (403, 404)


