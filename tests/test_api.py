from fastapi.testclient import TestClient
from salary_service.main import app

client = TestClient(app)


def test_auth():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_route():
    response = client.get("/salary")
    assert response.status_code == 401


def test_salary_with_token():
    auth_response = client.post(
        "/token",
        data={"username": "admin", "password": "secret"}
    )
    token = auth_response.json()["access_token"]

    response = client.get(
        "/salary",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200