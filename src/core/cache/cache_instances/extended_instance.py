import functools
from typing import Callable, Any
import hashlib
import msgpack
from .base_instance import CacheInstanceAbs


class CacheExtendedInstance(CacheInstanceAbs):

    @staticmethod
    def _hash_inputs(*args, **kwargs) -> str:
        try:
            serialized_args = tuple(args)
            serialized_kwargs = tuple(sorted(kwargs.items()))
            combined = str(serialized_args) + str(serialized_kwargs)
            return hashlib.sha256(combined.encode('utf-8')).hexdigest()[:16]  # Truncated hash for brevity
        except Exception as e:
            raise ValueError(f"Unable to hash inputs: {e}")
    
    @staticmethod
    def _serialize(data: Any) -> Any:
        try:
            return msgpack.dumps(data, use_bin_type=True)
        except Exception as e:
            raise ValueError(f"Serialization failed: {e}")
    
    @staticmethod
    def _deserialize(data: Any) -> Any:
        try:
            return msgpack.loads(data, raw=False)
        except Exception as e:
            raise ValueError(f"Deserialization failed: {e}")

    def cache(self, expire: int = 3600, prefix: str = "cache:") -> Callable[..., Any]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(function)
            async def wrapper(*args, **kwargs) -> Any:
                # Generate unique cache key
                unique_parameters = self._hash_inputs(*args, **kwargs)
                normalized_name = f"{prefix}{unique_parameters}{function.__module__}.{function.__qualname__}"

                # Try retrieving from cache
                if cache_response := await self.get(normalized_name):
                    try:
                        return self._deserialize(cache_response)
                    except Exception as e:
                        print(f"Cache miss or deserialization error: {e}")

                response = await function(*args, **kwargs)
                serialized_response = self._serialize(response)
                await self.set(normalized_name, serialized_response, ex=expire)

                return response
            return wrapper
        return decorator
