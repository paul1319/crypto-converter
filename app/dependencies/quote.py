from binance import AsyncClient
from dependency_injector import containers, providers
from redis.asyncio import Redis

from app.adapters.binance.adapter import BinanceAdapter, IBinanceAdapter
from app.consumers.quote import QuoteConsumer
from app.infrastructure.binance import init_binance_client
from app.infrastructure.redis import init_redis
from app.repositories.uow import IUnitOfWork, UnitOfWork
from app.settings import Settings


class QuoteAppContainer(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)

    # DB
    redis: providers.Resource[Redis] = providers.Resource(init_redis, settings=settings.provided.redis)
    unit_of_work: providers.ContextLocalSingleton[IUnitOfWork] = providers.ContextLocalSingleton(
        UnitOfWork, database=redis
    )

    # Clients
    binance_client: providers.Resource[AsyncClient] = providers.Resource(init_binance_client)

    # Adapters
    binance_adapter: providers.Singleton[IBinanceAdapter] = providers.Singleton(BinanceAdapter, client=binance_client)

    # Consumers
    quote_consumer: providers.Factory[QuoteConsumer] = providers.Factory(
        QuoteConsumer, uow=unit_of_work, adapter=binance_adapter, settings=settings.provided.quote
    )
