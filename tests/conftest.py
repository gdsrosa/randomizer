import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from src.randomizer.database import items_db, users_db
from src.randomizer.schemas import UserInDB
from src.randomizer.auth.service import get_password_hash
from src.randomizer.main import app


@pytest.fixture(autouse=True)
def clear_database():
    items_db._items.clear()
    users_db._users.clear()
    yield
    items_db._items.clear()
    users_db._users.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sync_client():
    return TestClient(app)


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_client(client: TestClient):
    users_db.add(UserInDB(id=uuid4(), username="testuser", hashed_password=get_password_hash("testpass123")))
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpass123"})
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
