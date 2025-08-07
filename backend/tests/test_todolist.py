from urllib import response


def test_create_todo_success(client, auth_header):
    payload = {
        "to_do": "Do homework",
        "description": "Complete math and science",
        "is_daily": True
    }

    response = client.post("api/todos", json=payload, headers=auth_header)
    data = response.get_json()
    print(data)
    print(response.status_code)
    print(response.get_json())
    assert response.status_code == 201
    assert data['to_do'] == "Do homework"
    assert data['description'] == "Complete math and science"
    assert data['is_daily'] is True
    assert 'list_id' in data
def test_get_todos(client, auth_header):
    # First, create a to-do
    client.post("api/todos", json={
        "to_do": "Study",
        "description": "Read history",
        "is_daily": False
    }, headers=auth_header)

    response = client.get("api/todos", headers=auth_header)
    data = response.get_json()
    print(data)
    print(response.status_code)
    assert response.status_code == 200
    assert 'todos' in data
    assert len(data['todos']) > 0
    
    
    
def test_update_todo(client, auth_header):
    # First, create a to-do
    post_response = client.post("api/todos", json={
        "to_do": "Clean room",
        "description": "Dust and sweep",
    }, headers=auth_header)

    todo_id = post_response.get_json()['list_id']
    print("Todo id is", todo_id)
    # Now update the to-do
    update_payload = {
        "list_id": todo_id,
        "to_do": "Clean bedroom",
        "description": "Include wardrobe",
        "is_done": True,
        "is_daily": True
    }

    put_response = client.put(f"api/todos/{todo_id}", json=update_payload, headers=auth_header)
    data = put_response.get_json()
    print(data)
    print(put_response.status_code)
    assert put_response.status_code == 200
    assert data['to_do'] == "Clean bedroom"
    assert data['is_done'] is True
    assert 'completion_date' in data and data['completion_date'] is not None
    
    
def test_delete_todo(client, auth_header):
    # Create a to-do first
    post_response = client.post("api/todos", json={
        "to_do": "Go running",
        "description": "Run 5km"
    }, headers=auth_header)

    todo_id = post_response.get_json()['list_id']

    # Delete the to-do
    delete_response = client.delete(f"api/todos/{todo_id}", headers=auth_header)
    assert delete_response.status_code == 200
    assert delete_response.get_json()['message'] == 'To-do item deleted successfully'

    # Confirm deletion
    get_response = client.get("api/todos", headers=auth_header)
    todos = get_response.get_json()['todos']
    assert not any(t['list_id'] == todo_id for t in todos)
    print(get_response.get_json())

def test_create_todo_missing_field(client, auth_header):
    payload = {
        "description": "This should fail"
    }

    response = client.post("api/todos", json=payload, headers=auth_header)
    assert response.status_code == 400
    assert "to_do is required" in response.get_json()['error']
    print(response.get_json())

def test_get_todo_invalid_date_format(client, auth_header):
    response = client.get("api/todos?date=2023-01-01", headers=auth_header)
    assert response.status_code == 400
    assert "Invalid date format" in response.get_json()['error']
    print(response.get_json())