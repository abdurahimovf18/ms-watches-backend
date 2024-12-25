from functools import wraps
from typing import Callable, Any, Optional

import hashlib
import orjson
from loguru import logger 

from .base_instance import CacheInstanceAbs
from .base_cache_service import BaseCacheService


class CacheExtendedInstance(CacheInstanceAbs):

    BaseCacheService = BaseCacheService

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.BaseCacheService.set_cache_instance(self)

    """
    A class that extends CacheInstanceAbs to provide caching functionality 
    using Redis, along with serialization and deserialization using orjson.
    """

    @staticmethod
    def _serialize(data: Any) -> bytes:
        """
        Serialize a Python object into a JSON-encoded bytes object using orjson.

        This method is responsible for converting Python objects into a byte format that
        can be stored in a cache (such as Redis). It ensures that the data is correctly
        serialized into a format that can be reliably stored and retrieved.

        Args:
            data (Any): The Python object to serialize.

        Returns:
            bytes: The JSON-encoded bytes object representing the serialized data.

        Raises:
            TypeError: If the data contains unsupported types that cannot be serialized.
        """
        try:
            return orjson.dumps(data)
        except Exception as e:
            raise TypeError(f"Serialization failed for data of type {type(data)}: {e}") from e

    @staticmethod
    def _deserialize(serialized_data: bytes) -> Any:
        """
        Deserialize a JSON-encoded bytes object into its original Python object using orjson.

        This method converts the byte representation of an object back into its original
        Python format. It's useful for retrieving cached data from Redis and converting
        it back to its usable form.

        Args:
            serialized_data (bytes): The serialized bytes object to deserialize.

        Returns:
            Any: The deserialized Python object.

        Raises:
            ValueError: If deserialization fails or the data format is invalid.
        """
        try:
            return orjson.loads(serialized_data)
        except Exception as e:
            raise ValueError("Deserialization failed. Invalid format or corrupted data.") from e

    def get_cache_name(self, prefix: str, *args: Any, **kwargs: Any) -> str:
        """
        Generate a unique cache key based on the provided prefix, arguments, and keyword arguments.

        This method ensures that a cache key is unique for each function call, using
        a combination of the function's arguments and keyword arguments. It hashes the
        combined data to generate a consistent yet unique key.

        Args:
            prefix (str): A string prefix to make the cache key more descriptive.
            args (Any): Positional arguments passed to the function.
            kwargs (Any): Keyword arguments passed to the function.

        Returns:
            str: A string representing the unique cache key generated.
        """
        # Serialize the arguments and keyword arguments to generate a consistent cache key
        key_data = f"{args}{sorted(kwargs.items())}"
        
        # Create a unique hash from the serialized data
        key_hash = hashlib.md5(key_data.encode()).hexdigest()  # Make sure it's encoded properly

        # Return the cache key using the provided prefix and the hash
        return f"{prefix}:{key_hash}"

    def cache_function(self, expiry: int = 15 * 60, prefix: Optional[str] = None) -> Callable:
        """
        Cache the result of a function call in Redis using a decorator.

        This decorator is used to cache the return value of a function for a specified
        period. It first checks if the data is available in the cache and returns the 
        cached data if present. If the data is not cached or if deserialization fails,
        it executes the function and stores the result in the cache.

        Args:
            expiry (int): The cache expiry time in seconds (default is 3600 seconds, or 1 hour).
            prefix (Optional[str]): An optional prefix for the cache key. If not provided, 
                                    the function's name will be used.

        Returns:
            Callable: A decorator that wraps the function with caching logic.

        Raises:
            RuntimeError: If there is a failure during the caching process (e.g., Redis issues).
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Use the function name as a prefix if none is provided
                _prefix = prefix or func.__name__

                # Generate a unique cache key based on the prefix and function parameters
                key = self.get_cache_name(_prefix, *args, **kwargs)

                # Try to fetch the cached data
                cached_data = await self.get(key)

                if cached_data:
                    try:
                        return self._deserialize(cached_data)
                    except (TypeError, ValueError) as e:
                        logger.error(f"Deserialization error: {str(e)}")
                        # Continue and execute the function if deserialization fails

                # Execute the function if the data is not cached
                result = await func(*args, **kwargs)

                try:
                    # Cache the result (serialized) with an expiry time
                    await self.set(key, self._serialize(result), ex=expiry)
                except Exception as e:
                    logger.error(f"Error during Redis set operation: {str(e)}")
                    raise RuntimeError("Failed to cache the result.") from e

                # Return the function result
                return result

            return wrapper
        return decorator

    @staticmethod    
    def no_op_decorator(func: Callable) -> Callable:
        return func
    
    def cache_method(
        self,
        expiry: int = 15 * 60,
        prefix: Optional[str] = None,
        is_classmethod: bool = True
    ) -> Callable:
        
        """
        A decorator method that applies caching to a function. It uses a cache function to store 
        the result of the decorated function and allows customization of the caching behavior 
        (expiry time, cache key prefix, and class method behavior).

        The decorator can be used on both instance methods and class methods, depending on the
        `is_classmethod` argument.

        Args:
            expiry (int): The expiry time of the cache in seconds. Defaults to 15 minutes (15 * 60).
            prefix (str | None): The prefix for the cache key. If `None`, no prefix is used.
            is_classmethod (bool): If `True`, the decorator is applied to class methods. If `False`, 
                                    it is applied to instance methods.

        Returns:
            Callable: A decorator that wraps the function with caching logic.

        Example:
            @cache_method(expiry=60, prefix="user_", is_classmethod=False)
            async def get_user_data(self, user_id: int):
                # Function logic here
                pass

        Notes:
            - The function being decorated must be asynchronous, as the wrapper is designed to
            handle asynchronous functions with `await`.
            - The caching behavior is determined by the `self.cache_function` method, which should
            define how the cache is applied (e.g., using an in-memory cache, Redis, etc.).
        """
        
        cf_decorator = self.cache_function(expiry=expiry, prefix=prefix)
        clsm = is_classmethod and classmethod or self.no_op_decorator

        def decorator(func):
            
            @clsm
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:

                cf_decorator_resp = await cf_decorator(func)(*args, **kwargs)
                return cf_decorator_resp
            return wrapper
        
        return decorator
