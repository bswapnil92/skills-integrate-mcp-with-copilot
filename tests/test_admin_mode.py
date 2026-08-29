from fastapi.testclient import TestClient

from src.app import app


def test_teacher_login_accepts_known_credentials():
    client = TestClient(app)
    response = client.post(
        "/login",
        json={"username": "teacher@mergington.edu", "password": "teacher123"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "teacher@mergington.edu"


def test_student_actions_are_blocked_without_login():
    client = TestClient(app)
    response = client.post(
        "/activities/Chess%20Club/signup?email=student@example.edu"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_teacher_cookie_allows_member_management():
    client = TestClient(app)
    login_response = client.post(
        "/login",
        json={"username": "teacher@mergington.edu", "password": "teacher123"},
    )
    assert login_response.status_code == 200

    response = client.post(
        "/activities/Chess%20Club/signup?email=student@example.edu",
    )

    assert response.status_code == 200
    assert "student@example.edu" in client.get("/activities").json()["Chess Club"]["participants"]
