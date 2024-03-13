from redis import ResponseError

from app.api.quotes.schemas import ConvertResponse
from app.errors.exceptions import QuotesNotFoundAppError, QuotesOutdatedAppError
from app.repositories.uow import IUnitOfWork
from app.settings import QuoteSettings
from app.utils.dt_utils import get_milliseconds_timestamp


class GetConversionView:
    def __init__(self, uow: IUnitOfWork, settings: QuoteSettings):
        self._uow = uow
        self._settings = settings

    async def __call__(
        self, amount: float, from_currency: str, to_currency: str, timestamp: int | None
    ) -> ConvertResponse:
        async with self._uow:
            if timestamp is None:
                timestamp, rate = await self._get_quote(from_currency=from_currency, to_currency=to_currency)
            else:
                timestamp, rate = await self._get_quote_timestamp(
                    from_currency=from_currency, to_currency=to_currency, timestamp=timestamp
                )

        if timestamp is None or rate is None:
            raise ValueError("'timestamp' and 'rate' are required")
        precision_rate = round(rate, 12)
        return ConvertResponse(amount=amount * precision_rate, rate=precision_rate)

    async def _get_quote(self, from_currency: str, to_currency: str) -> tuple[int, float]:
        ts = self._uow.session.ts()
        try:
            timestamp, rate = (await ts.get(key=f"quote:{from_currency}{to_currency}").execute())[0]
        except ResponseError:
            try:
                timestamp, rate = (await ts.get(key=f"quote:{to_currency}{from_currency}").execute())[0]
                rate = 1 / rate
            except ResponseError as e:
                raise QuotesNotFoundAppError from e
        if timestamp + self._settings.quote_outdated_secs * 1000 < get_milliseconds_timestamp():
            raise QuotesOutdatedAppError
        return timestamp, rate

    async def _get_quote_timestamp(self, from_currency: str, to_currency: str, timestamp: int) -> tuple[int, float]:
        ts = self._uow.session.ts()
        from_time = timestamp - self._settings.quote_outdated_secs * 1000
        try:
            result = (
                await ts.revrange(
                    key=f"quote:{from_currency}{to_currency}",
                    from_time=from_time,
                    to_time=timestamp,
                    count=1,
                ).execute()
            )[0]
            if not result:
                raise QuotesNotFoundAppError
            timestamp, rate = result[0]
        except ResponseError:
            try:
                result = (
                    await ts.revrange(
                        key=f"quote:{to_currency}{from_currency}",
                        from_time=from_time,
                        to_time=timestamp,
                        count=1,
                    ).execute()
                )[0]
                if not result:
                    raise QuotesNotFoundAppError
                timestamp, rate = result[0][0], 1 / result[0][1]
            except ResponseError as e:
                raise QuotesNotFoundAppError from e
        return timestamp, rate
