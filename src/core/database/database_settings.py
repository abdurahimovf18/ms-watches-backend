from src.core.base_settings import BaseEnvConsumer


class DatabaseEnvConsumer(BaseEnvConsumer):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


DB_ENV = DatabaseEnvConsumer()


DB_ASYNC_URL = (f"postgresql+asyncpg://{DB_ENV.DB_USER}:{DB_ENV.DB_PASSWORD}"
                f"@{DB_ENV.DB_HOST}:{DB_ENV.DB_PORT}/{DB_ENV.DB_NAME}")

DB_SYNC_URL = (f"postgresql+psycopg2://{DB_ENV.DB_USER}:{DB_ENV.DB_PASSWORD}"
                f"@{DB_ENV.DB_HOST}:{DB_ENV.DB_PORT}/{DB_ENV.DB_NAME}")
