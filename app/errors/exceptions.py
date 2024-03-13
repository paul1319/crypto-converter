from app.utils.exceptions import BaseAppException


class AppError(BaseAppException):
    message: str


class QuotesOutdatedAppError(AppError):
    message = "Quotes are outdated"


class QuotesNotFoundAppError(AppError):
    message = "Quotes not found"
