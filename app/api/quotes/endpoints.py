from decimal import Decimal
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import RequestValidationError

from app.api.models import APIResponse
from app.api.quotes.schemas import ConvertResponse
from app.dependencies.web_app import WebAppContainer
from app.utils.dt_utils import get_milliseconds_timestamp
from app.views.get_conversion import GetConversionView

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.get("/convert")
@inject
async def convert(
    amount: Annotated[Decimal, Query(description="Amount to convert", decimal_places=6, gt=0)],
    from_currency: Annotated[str, Query(description="Currency from", alias="from", min_length=1, max_length=15)],
    to_currency: Annotated[str, Query(description="Currency to", alias="to", min_length=1, max_length=15)],
    timestamp: Annotated[int | None, Query(description="UNIX timestamp in milliseconds")] = None,
    view: GetConversionView = Depends(Provide[WebAppContainer.get_conversion_view]),  # noqa: B008
) -> APIResponse[ConvertResponse]:
    if timestamp is not None and timestamp > get_milliseconds_timestamp():
        raise RequestValidationError("Timestamp can't be in the future")
    result = await view(
        amount=float(amount), from_currency=from_currency.upper(), to_currency=to_currency.upper(), timestamp=timestamp
    )
    return APIResponse(result=result)
