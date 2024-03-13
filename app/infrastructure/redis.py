from collections.abc import AsyncIterator

from redis.asyncio import Redis, from_url

from app.settings import RedisSettings


async def init_redis(settings: RedisSettings) -> AsyncIterator[Redis]:
    redis = await from_url(url=settings.url, db=settings.db, decode_responses=True)
    await redis.ping()
    yield redis
    await redis.aclose()
