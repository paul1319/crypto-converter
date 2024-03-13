from typing import Generic, TypeVar

from pydantic import BaseModel

from app.utils.model import AppBaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    result: T


class APIErrorResponse(AppBaseModel):
    message: str
