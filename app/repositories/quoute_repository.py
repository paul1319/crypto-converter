from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from redis.asyncio.client import Pipeline

from app.domain.quote import Quote
from app.settings import settings


class IQuoteRepository(Protocol):
    @abstractmethod
    async def add_quotes(self, quotes: Iterable[Quote]) -> None:
        pass


class QuoteRepository(IQuoteRepository):
    def __init__(self, session: Pipeline):
        self._session = session
        self._ts = session.ts()

    async def add_quotes(self, quotes: Iterable[Quote]) -> None:
        for q in quotes:
            await self._ts.add(
                key=f"quote:{q.symbol}",
                value=q.rate,
                timestamp="*",
                duplicate_policy="block",
                retention_msecs=settings.quote.quote_ttl_secs * 1000,
            )
