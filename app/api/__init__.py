from fastapi import FastAPI

from app.api.quotes.endpoinst import router as quotes_router

API_V1_STR = "/api/v1"


def init_routers(app: FastAPI) -> None:
    app.include_router(quotes_router, prefix=API_V1_STR)
