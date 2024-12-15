from src.core.base_settings import BaseEnvConsumer


class CacheEnvConsumer(BaseEnvConsumer):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


CACHE_ENV = CacheEnvConsumer()
