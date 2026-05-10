import pytest
from fastapi.testclient import TestClient
from src.randomizer.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestRegisterEndpoint:
    def test_register_user_returns_id(self, client: TestClient):
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "password": "password123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "newuser"

    def test_register_user_auto_generates_id(self, client: TestClient):
        response1 = client.post(
            "/auth/register",
            json={"username": "user1", "password": "password123"},
        )
        response2 = client.post(
            "/auth/register",
            json={"username": "user2", "password": "password123"},
        )
        id1 = response1.json()["id"]
        id2 = response2.json()["id"]
        assert id1 != id2

    def test_register_long_password(self, client: TestClient):
        long_password = "a" * 100
        response = client.post(
            "/auth/register",
            json={"username": "longpwuser", "password": long_password},
        )
        assert response.status_code == 201

    def test_register_multibyte_password_can_login(self, client: TestClient):
        password = "pässwörd🔥emoji😀" + "a" * 60
        register_resp = client.post(
            "/auth/register",
            json={"username": "unicodepw", "password": password},
        )
        assert register_resp.status_code == 201

        login_resp = client.post(
            "/auth/login",
            json={"username": "unicodepw", "password": password},
        )
        assert login_resp.status_code == 200
        assert "access_token" in login_resp.json()

    def test_register_duplicate_username(self, client: TestClient):
        client.post(
            "/auth/register",
            json={"username": "dupuser", "password": "password123"},
        )
        response = client.post(
            "/auth/register",
            json={"username": "dupuser", "password": "password456"},
        )
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"]