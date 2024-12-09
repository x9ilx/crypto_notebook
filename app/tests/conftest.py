import pytest
import pytest_asyncio # noqa
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.db import Base, get_async_session # noqa
from core.users import current_user # noqa
from main import app # noqa
from schemas.users import UserCreate # noqa

pytest_plugins = [
    'tests.fixtures.user',
    'tests.fixtures.currency'
]


DB_URL = 'sqlite+aiosqlite:///:memory:'
ENGINE = create_async_engine(DB_URL, connect_args={'check_same_thread': False})
TESTING_SESSION_LOCAL = sessionmaker(
    autocommit=False, autoflush=False, bind=ENGINE, class_=AsyncSession
)


async def database_action_with_engine(action):
    async with ENGINE.begin() as connection:
        await connection.run_sync(action)


async def override_db():
    async with TESTING_SESSION_LOCAL() as session:
        yield session


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(autouse=True)
async def init_db():
    await database_action_with_engine(Base.metadata.create_all)
    yield
    await database_action_with_engine(Base.metadata.drop_all)


@pytest.fixture
async def mixer(override_db):
    async with override_db() as session:
        return _mixer(session=session, commit=True)