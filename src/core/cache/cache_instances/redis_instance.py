from typing import Type
from redis.asyncio import Redis

from .extended_instance import CacheExtendedInstance


class RedisCacheInstance(Redis, CacheExtendedInstance):
    def __init__(self, host='localhost', port=6379, db=0, *args, **kwargs):
        super().__init__(host=host, port=port, db=db, *args, **kwargs)
        super(CacheExtendedInstance).__init__(*args, **kwargs)


def get_instance(host='localhost', port=6379, db=0, *args, **kwargs) -> Type[RedisCacheInstance]:
    return RedisCacheInstance(host=host, port=port, db=db, *args, **kwargs)
    