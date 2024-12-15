from abc import ABC
from .extended_instance import CacheExtendedInstance
from redis.asyncio import Redis
from typing import Type

class RedisCacheInstance(Redis, CacheExtendedInstance):
    def __init__(self, host='localhost', port=6379, db=0, *args, **kwargs):
        # Initialize the parent Redis class
        super().__init__(host=host, port=port, db=db, *args, **kwargs)


def get_instance(host='localhost', port=6379, db=0, *args, **kwargs) -> Type[RedisCacheInstance]:
    return RedisCacheInstance(host=host, port=port, db=db, *args, **kwargs)
