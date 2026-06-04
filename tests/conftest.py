import json
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport
from src.api.Dependencies import get_db
from src.config import settings
from src.main import app
from src.models import *
from src.database import Base, engine_null_pull, async_session_maker_null_pull
from src.models.user import Role
from src.schemas.books import AddBook
from src.schemas.user import UserRole
from src.utils.dbmanager import DBManager
from src.init import redis_conn as r

@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager]:
    async for db in get_db_null_pull():
        yield db


async def get_db_null_pull():
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pull

@pytest.fixture(scope="session", autouse=True)
async def mock_redis():
    r.redis = AsyncMock()
    yield
    r.redis = None


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"
    FastAPICache.init(InMemoryBackend())
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/books_mock.json") as file:
        books = json.load(file)
    books = [AddBook.model_validate(book) for book in books]
    async with DBManager(session_factory=async_session_maker_null_pull) as _db:
        await _db.books.add_bulk(books)
        await _db.commit()

@pytest.fixture(scope="session")
async def ac():
    async with (AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
                as ac):
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def reg_client(ac, async_main):
    await ac.post("/auth/register",
                  json={"email": "admin@gmail.com",
                        "password": "admin1234"
                        }
                  )

@pytest.fixture(scope="session")
async def set_admin_user(reg_client):
    data = UserRole(role=Role.ADMIN)
    async with DBManager(session_factory=async_session_maker_null_pull) as _db:
        await _db.user.patch(data, id=1)
        await _db.commit()


@pytest.fixture(scope="session")
async def login_client(set_admin_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac


