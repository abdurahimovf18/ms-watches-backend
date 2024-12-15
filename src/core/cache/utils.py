import redis.asyncio as redis
import json
import hashlib
from functools import wraps
import asyncio

# Connect to Redis (make sure Redis is running)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_decorator(expiry=3600):
    """
    Decorator to cache function output in Redis.
    :param expiry: Cache expiry time in seconds (default 1 hour)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hashlib.md5(json.dumps((args, kwargs), sort_keys=True).encode()).hexdigest()}"

            cached_data = await redis_client.get(key)

            if cached_data:
                return _deserialize(cached_data)

            result = await func(*args, **kwargs)

            await redis_client.setex(key, expiry, _serialize(result))

            return result

        return wrapper

    return decorator


def _serialize(data):
    """
    Serializes the result (whether tuple, list, or dict) to a JSON string.
    """
    if isinstance(data, (tuple, list, dict)):
        return json.dumps(data)
    raise ValueError(f"Unsupported type: {type(data)}")


def _deserialize(serialized_data):
    """
    Deserializes the result from a JSON string back to its original type (tuple, list, or dict).
    """
    return json.loads(serialized_data)
