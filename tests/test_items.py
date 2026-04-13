from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from src.randomizer.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestItemEndpoints:
    def test_create_item_success(self, client: TestClient):
        response = client.post("/items", json={"name": "Test Item"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item created successfully."
        assert data["item"] == "Test Item"

    def test_create_item_duplicate_name(self, client: TestClient):
        client.post("/items", json={"name": "Duplicate Item"})
        response = client.post("/items", json={"name": "Duplicate Item"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Item already exists."

    def test_create_item_empty_name(self, client: TestClient):
        response = client.post("/items", json={"name": ""})
        assert response.status_code == 422

    def test_create_item_long_name(self, client: TestClient):
        long_name = "a" * 101
        response = client.post("/items", json={"name": long_name})
        assert response.status_code == 422

    def test_get_randomized_items_empty(self, client: TestClient):
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["original_order"] == []
        assert data["randomized_order"] == []
        assert data["count"] == 0

    def test_get_randomized_items_with_items(self, client: TestClient):
        client.post("/items", json={"name": "Item 1"})
        client.post("/items", json={"name": "Item 2"})
        client.post("/items", json={"name": "Item 3"})

        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert len(data["original_order"]) == 3
        assert len(data["randomized_order"]) == 3
        assert {item["name"] for item in data["original_order"]} == {
            "Item 1",
            "Item 2",
            "Item 3",
        }

    def test_update_item_success(self, client: TestClient):
        client.post("/items", json={"name": "Original Item"})
        item_id = str(
            next(
                item["id"]
                for item in client.get("/items").json()["original_order"]
                if item["name"] == "Original Item"
            )
        )

        response = client.put(f"/items/{item_id}", json={"name": "New Name"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item updated successfully"
        assert data["old_item"] == "Original Item"
        assert data["new_item"] == "New Name"

    def test_update_item_not_found(self, client: TestClient):
        fake_id = str(uuid4())
        response = client.put(f"/items/{fake_id}", json={"name": "New Name"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"

    def test_update_item_duplicate_name(self, client: TestClient):
        client.post("/items", json={"name": "Item A"})
        client.post("/items", json={"name": "Item B"})

        item_b_id = str(
            next(
                item["id"]
                for item in client.get("/items").json()["original_order"]
                if item["name"] == "Item B"
            )
        )

        response = client.put(f"/items/{item_b_id}", json={"name": "Item A"})
        assert response.status_code == 409
        assert response.json()["detail"] == "An item with that name already exists"

    def test_update_item_same_name(self, client: TestClient):
        client.post("/items", json={"name": "Same Name"})

        item_id = str(
            next(
                item["id"]
                for item in client.get("/items").json()["original_order"]
                if item["name"] == "Same Name"
            )
        )

        response = client.put(f"/items/{item_id}", json={"name": "Same Name"})
        assert response.status_code == 200

    def test_delete_item_success(self, client: TestClient):
        client.post("/items", json={"name": "To Delete"})
        item_id = str(
            next(
                item["id"]
                for item in client.get("/items").json()["original_order"]
                if item["name"] == "To Delete"
            )
        )

        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item deleted successfully"
        assert data["deleted_item_id"] == item_id
        assert data["remaining_items_count"] == 0

    def test_delete_item_not_found(self, client: TestClient):
        fake_id = str(uuid4())
        response = client.delete(f"/items/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"

    def test_delete_item_updates_count(self, client: TestClient):
        client.post("/items", json={"name": "Keep 1"})
        client.post("/items", json={"name": "Keep 2"})
        client.post("/items", json={"name": "Delete Me"})

        item_id = str(
            next(
                item["id"]
                for item in client.get("/items").json()["original_order"]
                if item["name"] == "Delete Me"
            )
        )

        response = client.delete(f"/items/{item_id}")
        assert response.json()["remaining_items_count"] == 2
