from redis.asyncio import Redis


class RedisHelper:
    def __init__(self, client: Redis):
        self._client = client
        self._ts = client.ts()

    async def cleanup_db(self) -> None:
        await self._client.flushall()

    async def add_quote(
        self, from_currency: str, to_currency: str, rate: float, timestamp: int | None = None, ttl_secs: int = 500
    ) -> None:
        await self._ts.add(
            key=f"quote:{from_currency}{to_currency}",
            value=rate,
            timestamp=timestamp if timestamp is not None else "*",
            duplicate_policy="block",
            retention_msecs=ttl_secs * 1000,
        )
