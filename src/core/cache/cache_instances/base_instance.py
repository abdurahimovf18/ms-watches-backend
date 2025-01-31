

class CacheInstanceAbs:
    async def get(self, key: str, *args, **kwargs):
        raise NotImplementedError("CacheInstanceAbs must implement the 'get' method")

    async def set(self, key: str, value, ex: int = None, px: int = None, nx: bool = False, xx: bool = False, *args, **kwargs):
        raise NotImplementedError("CacheInstanceAbs must implement the 'set' method")

    async def delete(self, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'delete' method")

    async def expire(self, key: str, time: int):
        raise NotImplementedError("CacheInstanceAbs must implement the 'expire' method")

    async def ttl(self, key: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'ttl' method")

    async def keys(self, pattern: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'keys' method")

    async def mget(self, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'mget' method")

    async def mset(self, mapping: dict):
        raise NotImplementedError("CacheInstanceAbs must implement the 'mset' method")

    async def incr(self, key: str, amount: int = 1):
        raise NotImplementedError("CacheInstanceAbs must implement the 'incr' method")

    async def decr(self, key: str, amount: int = 1):
        raise NotImplementedError("CacheInstanceAbs must implement the 'decr' method")

    async def flushdb(self):
        raise NotImplementedError("CacheInstanceAbs must implement the 'flushdb' method")

    async def hget(self, name: str, key: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hget' method")

    async def hset(self, name: str, key: str, value):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hset' method")

    async def hmget(self, name: str, keys: list):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hmget' method")

    async def hmset(self, name: str, mapping: dict):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hmset' method")

    async def hdel(self, name: str, *keys: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'hdel' method")

    async def lpush(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'lpush' method")

    async def rpush(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'rpush' method")

    async def lpop(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'lpop' method")

    async def rpop(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'rpop' method")

    async def llen(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'llen' method")

    async def smembers(self, name: str):
        raise NotImplementedError("CacheInstanceAbs must implement the 'smembers' method")

    async def sadd(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'sadd' method")

    async def srem(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'srem' method")

    async def zadd(self, name: str, mapping: dict, nx: bool = False, xx: bool = False, ch: bool = False, incr: bool = False):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zadd' method")

    async def zrange(self, name: str, start: int, end: int, desc: bool = False, withscores: bool = False, byscore: bool = False, score_cast_func=None):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zrange' method")

    async def zrem(self, name: str, *values):
        raise NotImplementedError("CacheInstanceAbs must implement the 'zrem' method")
    