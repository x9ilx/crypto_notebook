import pytest
from conftest import app, current_user, get_async_session, override_db
from httpx import ASGITransport, AsyncClient

from models.user import User


REGISTER_URL = '/auth/register'


user = User(
    id=100,
    email='test@test.test',
    hashed_password='test_password0',
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

user2 = User(
    id=200,
    email='test2@test2.test2',
    hashed_password='test_password0',
    is_active=True,
    is_verified=True,
    is_superuser=False,
)


@pytest.fixture
async def auth_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: user
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client


@pytest.fixture
async def noauth_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client
