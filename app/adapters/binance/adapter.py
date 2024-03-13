from abc import abstractmethod
from asyncio import Protocol

from binance import AsyncClient

from app.adapters.binance.schemas import BAQuote


class IBinanceAdapter(Protocol):
    @abstractmethod
    async def get_quotes(self) -> list[BAQuote]:
        pass


class BinanceAdapter(IBinanceAdapter):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get_quotes(self) -> list[BAQuote]:
        ticker_data = await self._client.get_all_tickers()
        return [BAQuote(symbol=t["symbol"], rate=float(t["price"])) for t in ticker_data]
