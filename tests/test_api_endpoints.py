import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_list_students(client):
    response = client.get("/api/students")
    assert response.status_code == 200
    assert response.get_json()["count"] == 2


def test_list_courses(client):
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.get_json()["count"] == 6


def test_enroll_endpoint(client):
    response = client.post(
        "/api/enrollments",
        json={"student_id": "S101", "course_id": "CS101"},
    )
    assert response.status_code == 201
    assert response.get_json()["enrollment"]["status"] == "ACTIVE"


def test_credit_limit_returns_conflict(client):
    for course in ["CS101", "CS102", "MA101", "PH101"]:
        client.post(
            "/api/enrollments",
            json={"student_id": "S101", "course_id": course},
        )
    response = client.post(
        "/api/enrollments",
        json={"student_id": "S101", "course_id": "EN101"},
    )
    assert response.status_code == 409
    assert "Credit limit exceeded" in response.get_json()["error"]


def test_unknown_student_returns_not_found(client):
    response = client.post(
        "/api/enrollments",
        json={"student_id": "S999", "course_id": "CS101"},
    )
    assert response.status_code == 404
