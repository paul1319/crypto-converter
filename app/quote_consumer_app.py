import asyncio
import signal

from app.dependencies.quote import QuoteAppContainer


class QuoteConsumerApp:
    def __init__(self) -> None:
        self._container = QuoteAppContainer()

    async def run(self) -> None:
        if coro := self._container.redis.init():
            await coro

        if coro := self._container.binance_client.init():
            await coro

        consumer = await self._container.quote_consumer()  # type: ignore[misc]

        loop = asyncio.get_running_loop()
        for sig in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(consumer.shutdown()))  # type: ignore[misc]

        await consumer.run()

        if coro := self._container.shutdown_resources():
            await coro
