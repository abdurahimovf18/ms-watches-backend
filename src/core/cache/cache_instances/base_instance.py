from abc import ABC, abstractmethod


class CacheInstanceAbs(ABC):
    @abstractmethod
    async def get(self, key: str, *args, **kwargs):
        raise NotImplementedError("CacheInstanceAbs must implement the 'get' method")

    @abstractmethod
    async def set(self, key: str, value, ex: int = None, px: int = None, nx: bool = False, xx: bool = False, *args, **kwargs):
        raise NotImplementedError("CacheInstanceAbs must implement the 'set' method")

    @abstractmethod
    async def delete(self, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'delete' method")

    @abstractmethod
    async def expire(self, key: str, time: int):
        raise NotImplementedError("CacheInstanceAbs must implement the 'expire' method")

    @abstractmethod
    async def ttl(self, key: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'ttl' method")

    @abstractmethod
    async def keys(self, pattern: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'keys' method")

    @abstractmethod
    async def mget(self, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'mget' method")

    @abstractmethod
    async def mset(self, mapping: dict):
        raise NotImplementedError("CacheInstanceAbs must implement the 'mset' method")

    @abstractmethod
    async def incr(self, key: str, amount: int = 1):
        raise NotImplementedError("CacheInstanceAbs must implement the 'incr' method")

    @abstractmethod
    async def decr(self, key: str, amount: int = 1):
        raise NotImplementedError("CacheInstanceAbs must implement the 'decr' method")

    @abstractmethod
    async def flushdb(self):
        raise NotImplementedError("CacheInstanceAbs must implement the 'flushdb' method")

    @abstractmethod
    async def hget(self, name: str, key: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hget' method")

    @abstractmethod
    async def hset(self, name: str, key: str, value):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hset' method")

    @abstractmethod
    async def hmget(self, name: str, keys: list):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hmget' method")

    @abstractmethod
    async def hmset(self, name: str, mapping: dict):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hmset' method")

    @abstractmethod
    async def hdel(self, name: str, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hdel' method")

    @abstractmethod
    async def lpush(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'lpush' method")

    @abstractmethod
    async def rpush(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'rpush' method")

    @abstractmethod
    async def lpop(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'lpop' method")

    @abstractmethod
    async def rpop(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'rpop' method")

    @abstractmethod
    async def llen(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'llen' method")

    @abstractmethod
    async def smembers(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'smembers' method")

    @abstractmethod
    async def sadd(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'sadd' method")

    @abstractmethod
    async def srem(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'srem' method")

    @abstractmethod
    async def zadd(self, name: str, mapping: dict, nx: bool = False, xx: bool = False, ch: bool = False, incr: bool = False):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zadd' method")

    @abstractmethod
    async def zrange(self, name: str, start: int, end: int, desc: bool = False, withscores: bool = False, byscore: bool = False, score_cast_func=None):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zrange' method")

    @abstractmethod
    async def zrem(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zrem' method")
    