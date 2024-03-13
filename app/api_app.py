from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import init_routers
from app.api.errors.handlers import register_exception_handlers
from app.dependencies.web_app import WebAppContainer


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    container = WebAppContainer()
    if coro := container.redis.init():
        await coro
    yield
    if coro := container.redis.shutdown():
        await coro


def build_api_app() -> FastAPI:
    app = FastAPI(title="Currency Conversion API", version="0.1.0", lifespan=lifespan)
    init_routers(app)
    register_exception_handlers(app)
    return app
