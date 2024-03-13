from abc import abstractmethod
from types import TracebackType
from typing import Protocol

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

from app.repositories.quoute_repository import IQuoteRepository, QuoteRepository


class IUnitOfWork(Protocol):
    @property
    @abstractmethod
    def session(self) -> Pipeline:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> None:
        pass

    @abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType
    ) -> None:
        pass

    @property
    @abstractmethod
    def quote_repository(self) -> IQuoteRepository:
        pass


class UnitOfWork(IUnitOfWork):
    def __init__(self, database: Redis):
        self._database = database
        self._session: Pipeline | None = None

    @property
    def session(self) -> Pipeline:
        if not self._session:
            raise RuntimeError("Session not initialized")
        return self._session

    async def commit(self) -> None:
        await self.session.execute()

    async def rollback(self) -> None:
        await self.session.reset()

    async def __aenter__(self) -> None:
        self._session = await self._database.pipeline(transaction=True).__aenter__()

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType
    ) -> None:
        await self.session.__aexit__(None, None, None)

    @property
    def quote_repository(self) -> IQuoteRepository:
        return QuoteRepository(session=self.session)
