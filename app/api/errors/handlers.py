from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette import status

from app.api.models import APIErrorResponse
from app.errors.exceptions import AppError, QuotesNotFoundAppError, QuotesOutdatedAppError


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)


def make_api_error_response(http_status_code: int, message: str) -> ORJSONResponse:
    return ORJSONResponse(status_code=http_status_code, content=jsonable_encoder(APIErrorResponse(message=message)))


def app_error_handler(_: Request, exc: AppError) -> ORJSONResponse:
    if isinstance(exc, QuotesOutdatedAppError):
        return make_api_error_response(http_status_code=status.HTTP_400_BAD_REQUEST, message=exc.message)
    elif isinstance(exc, QuotesNotFoundAppError):
        return make_api_error_response(http_status_code=status.HTTP_404_NOT_FOUND, message=exc.message)

    logger.exception(exc)
    return make_api_error_response(
        http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error"
    )


def validation_exception_handler(_: Request, exc: RequestValidationError) -> ORJSONResponse:
    return make_api_error_response(http_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=f"{exc.errors()}")


def unhandled_exception_handler(_: Request, exc: Exception) -> ORJSONResponse:
    logger.exception(exc)
    return make_api_error_response(
        http_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error"
    )
