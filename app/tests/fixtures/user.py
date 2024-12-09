import pytest
from conftest import app, current_user, get_async_session, override_db
from httpx import AsyncClient, ASGITransport

from models.user import User


user = User(
    id=100,
    is_active=True,
    is_verified=True,
    is_superuser=False
)


@pytest.fixture
async def auth_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: user
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture
async def noauth_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client
