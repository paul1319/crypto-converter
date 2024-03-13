import asyncio

from loguru import logger

from app.adapters.binance.adapter import IBinanceAdapter
from app.domain.quote import Quote
from app.dto.symbol import AddQuoteDTO
from app.repositories.uow import IUnitOfWork
from app.settings import QuoteSettings


class QuoteConsumer:
    def __init__(self, uow: IUnitOfWork, adapter: IBinanceAdapter, settings: QuoteSettings):
        self._uow = uow
        self._adapter = adapter
        self._settings = settings

        self._shutdown_event = asyncio.Event()
        self._is_shutdown = asyncio.Event()

    async def run(self) -> None:
        logger.info("QuoteConsumer is starting...")
        self._shutdown_event.clear()
        self._is_shutdown.clear()
        while True:
            try:
                logger.info("QuoteConsumer getting quotes data...")
                await self._update_quotes()
                logger.info("QuoteConsumer got quotes data")

                sleep = asyncio.create_task(asyncio.sleep(self._settings.update_quotes_interval_secs))
                wait_shutdown = asyncio.create_task(self._shutdown_event.wait())
                done, pending = await asyncio.wait({sleep, wait_shutdown}, return_when=asyncio.FIRST_COMPLETED)
                if wait_shutdown in done:
                    sleep.cancel()
                    self._is_shutdown.set()
                    break
                if sleep in done:
                    wait_shutdown.cancel()
            except Exception as e:
                logger.exception("QuoteConsumer crashed:", e)
                await asyncio.sleep(3)

    async def _update_quotes(self) -> None:
        tickers_data = await self._adapter.get_quotes()
        async with self._uow:
            await self._uow.quote_repository.add_quotes(
                quotes=[Quote.add(dto=AddQuoteDTO(symbol=t.symbol, rate=t.rate)) for t in tickers_data]
            )
            await self._uow.commit()

    async def shutdown(self) -> None:
        logger.info("QuoteConsumer is stopping...")
        self._shutdown_event.set()
        await self._is_shutdown.wait()
        logger.info("QuoteConsumer is stopped")
