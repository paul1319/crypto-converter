import asyncio

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import from_url

from app.api_app import build_api_app
from app.settings import settings
from tests.functional.utils.app_client import AppClient
from tests.functional.utils.redis_helper import RedisHelper


# Pytest magic, nothing works without this fixture
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    if not loop.is_closed():
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_helper() -> RedisHelper:
    client = redis = await from_url(url=settings.redis.url, db=settings.redis.db, decode_responses=True)
    await redis.ping()
    redis_helper = RedisHelper(client=client)
    yield redis_helper
    await client.aclose()


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db(redis_helper) -> None:
    await redis_helper.cleanup_db()
    yield


@pytest.fixture(scope="session")
def api_application() -> FastAPI:
    return build_api_app()


@pytest_asyncio.fixture(scope="session")
async def test_client(api_application) -> AsyncClient:
    async with LifespanManager(app=api_application) as manager:
        async with AsyncClient(transport=ASGITransport(app=manager.app), base_url="http://test") as test_client:
            yield test_client


@pytest_asyncio.fixture(scope="session")
def app_client(test_client) -> AppClient:
    yield AppClient(test_client=test_client)
