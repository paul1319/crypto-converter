from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    host: str
    port: int
    reload: bool

    model_config = SettingsConfigDict(env_prefix="SRV_", env_file=".env")


class LoggingSettings(BaseSettings):
    level: str

    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env")


class RedisSettings(BaseSettings):
    url: str
    db: int

    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=".env")


class QuoteSettings(BaseSettings):
    update_quotes_interval_secs: int
    quote_ttl_secs: int
    quote_outdated_secs: int

    model_config = SettingsConfigDict(env_prefix="QT_", env_file=".env")


class Settings(BaseSettings):
    load_dotenv()
    server: ServerSettings = ServerSettings()
    logging: LoggingSettings = LoggingSettings()
    redis: RedisSettings = RedisSettings()
    quote: QuoteSettings = QuoteSettings()


settings = Settings()
