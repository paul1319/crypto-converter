from dependency_injector import containers, providers
from redis.asyncio import Redis

from app.infrastructure.redis import init_redis
from app.repositories.uow import IUnitOfWork, UnitOfWork
from app.settings import Settings
from app.views.get_conversion import GetConversionView


class WebAppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api", __name__])
    settings = providers.Singleton(Settings)

    # DB
    redis: providers.Resource[Redis] = providers.Resource(init_redis, settings=settings.provided.redis)
    unit_of_work: providers.ContextLocalSingleton[IUnitOfWork] = providers.ContextLocalSingleton(
        UnitOfWork, database=redis
    )

    # Views
    get_conversion_view: providers.Factory[GetConversionView] = providers.Factory(
        GetConversionView, uow=unit_of_work, settings=settings.provided.quote
    )
