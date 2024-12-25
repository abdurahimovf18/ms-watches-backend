from datetime import timedelta

from src.core.base_settings import BaseEnvConsumer


class AuthEnvConsumer(BaseEnvConsumer):
    SECRET_KEY: str 
    
    JWT_ALGORITHM: str 
    JWT_EXPIRE_MINUTE: int 
    
    JWT_REFRESH_EXPIRE_DAYS: int 
    ISSUER: str
    AUDIENCE: str

    @property
    def JWT_EXPIRE_TIME(self) -> timedelta:
        return timedelta(minutes=self.JWT_EXPIRE_MINUTE)


ENV_DATA = AuthEnvConsumer()

