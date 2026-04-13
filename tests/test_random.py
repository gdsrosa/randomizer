import pytest
from fastapi.testclient import TestClient
from src.randomizer.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestRandomNumberEndpoints:
    def test_home(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Randomizer API!"}

    def test_get_random_number_positive(self, client: TestClient):
        response = client.get("/random/10")
        assert response.status_code == 200
        data = response.json()
        assert "random_number" in data
        assert data["max_value"] == 10
        assert 1 <= data["random_number"] <= 10

    def test_get_random_number_zero(self, client: TestClient):
        response = client.get("/random/0")
        assert response.status_code == 200
        assert response.json() == {"error": "max_value must be greater than 0."}

    def test_get_random_number_negative(self, client: TestClient):
        response = client.get("/random/-5")
        assert response.status_code == 200
        assert response.json() == {"error": "max_value must be greater than 0."}

    def test_get_random_number_between_defaults(self, client: TestClient):
        response = client.get("/random-between/")
        assert response.status_code == 200
        data = response.json()
        assert data["min_value"] == 1
        assert data["max_value"] == 99
        assert 1 <= data["random_number"] <= 99

    def test_get_random_number_between_custom(self, client: TestClient):
        response = client.get("/random-between/?min_value=50&max_value=100")
        assert response.status_code == 200
        data = response.json()
        assert data["min_value"] == 50
        assert data["max_value"] == 100
        assert 50 <= data["random_number"] <= 100

    def test_get_random_number_between_min_equals_max(self, client: TestClient):
        response = client.get("/random-between/?min_value=42&max_value=42")
        assert response.status_code == 200
        data = response.json()
        assert data["random_number"] == 42

    def test_get_random_number_between_invalid_range(self, client: TestClient):
        response = client.get("/random-between/?min_value=100&max_value=50")
        assert response.status_code == 400
        assert (
            "min_value must be less than or equal to max_value"
            in response.json()["detail"]
        )

    def test_get_random_number_between_below_minimum(self, client: TestClient):
        response = client.get("/random-between/?min_value=0")
        assert response.status_code == 422

    def test_get_random_number_between_above_maximum(self, client: TestClient):
        response = client.get("/random-between/?max_value=1001")
        assert response.status_code == 422
