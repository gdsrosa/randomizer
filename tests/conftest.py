import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from src.randomizer.database import items_db
from src.randomizer.main import app


@pytest.fixture(autouse=True)
def clear_database():
    items_db._items.clear()
    yield
    items_db._items.clear()


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
