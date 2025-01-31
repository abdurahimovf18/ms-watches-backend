from functools import wraps
from typing import Callable, Any, Optional, Sequence, Type, Literal
from collections.abc import Mapping
from decimal import Decimal

import hashlib
import orjson
from loguru import logger 

from sqlalchemy.sql.elements import quoted_name
from pydantic import BaseModel

from .base_instance import CacheInstanceAbs
from .base_cache_service import BaseCacheService


class Undefined: pass

from typing import Any
from pydantic import BaseModel
from decimal import Decimal


class DataSerializer:
    """
    A class responsible for serializing and deserializing data using orjson.
    It handles various data types with custom methods to ensure correct serialization.
    """
    
    def __init__(self, data: Any):
        """
        Initializes the DataSerializer with data to be serialized or deserialized.
        
        Args:
            data (Any): The data to be serialized or deserialized.
        """
        self.data = data

        # Mapping of types to their respective handling methods.
        self.methods = {
            BaseModel: self.handle_pydantic,
            Decimal: self.handle_decimal,
        }
        
    @property
    def serialized(self) -> Any:
        """
        Serializes the data using orjson's dumps method. If the data contains 
        custom types, the `handle_orjson_defaults` method is used to handle them.
        
        Returns:
            Any: The serialized data in JSON format.
        
        Raises:
            RuntimeError: If an error occurs during serialization.
        """
        try:
            return orjson.dumps(self.data, default=self.handle_orjson_defaults)
        except Exception as e:
            raise RuntimeError(
                f"Error on serializing data for orjson.dumps method\n"
                f"Data: {self.data}\n"
                f"Data Type: {type(self.data)}\n"
                f"Module: {self.__module__}\n\n"
                f"Error: {e}"
            ) from e

    @property
    def deserialized(self) -> Any:
        """
        Deserializes the data using orjson's loads method.
        
        Returns:
            Any: The deserialized data.
        
        Raises:
            RuntimeError: If an error occurs during deserialization.
        """
        try:
            return orjson.loads(self.data)
        except Exception as e:
            raise RuntimeError(
                f"Error on deserializing data for orjson.loads method\n"
                f"Data: {self.data}\n"
                f"Data Type: {type(self.data)}\n"
                f"Module: {self.__module__}\n\n"
                f"Error: {e}"
            ) from e

    @staticmethod
    def handle_pydantic(instance: BaseModel) -> dict:
        """
        Handles serialization of Pydantic BaseModel instances by calling the 
        `model_dump` method to convert the instance to a dictionary.
        
        Args:
            instance (BaseModel): The Pydantic model instance to serialize.
        
        Returns:
            dict: A dictionary representation of the Pydantic model.
        """
        return instance.model_dump()
    
    @staticmethod
    def handle_decimal(instance: Decimal) -> str:
        """
        Handles serialization of Decimal instances by converting them to strings.
        
        Args:
            instance (Decimal): The Decimal instance to serialize.
        
        Returns:
            str: A string representation of the Decimal value.
        """
        return str(instance)
            
    def handle_orjson_defaults(self, instance: Any):
        """
        Handles custom serialization for types that are not natively serializable 
        by orjson by checking the type of the instance and applying the corresponding method.
        
        Args:
            instance (Any): The instance to serialize.
        
        Returns:
            Any: The serialized form of the instance.
        
        Raises:
            TypeError: If no handler is available for the type of the instance.
        """
        for type_, method in self.methods.items():
            if isinstance(instance, type_):
                return method(instance)
        raise TypeError(f"Unsupported type: {type(instance)}")


class CacheExtendedInstance(CacheInstanceAbs):
    """
    A class that extends CacheInstanceAbs to provide caching functionality 
    using Redis, along with serialization and deserialization using orjson.
    """

    CacheService = BaseCacheService

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.CacheService.set_cache_instance(self)

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

    def cache_function(self, 
                       expiry: int = 15 * 60, 
                       prefix: Optional[str] = None,
                       not_cache_on_type: Sequence[Type] | Type | Undefined = Undefined) -> Callable:
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
            not_cache_on_type (Sequence[Type] | Type | Undefined): An optional parameter used to restinct
                                                                 cache when edge type comes as result

        Returns:
            Callable: A decorator that wraps the function with caching logic.

        Raises:
            RuntimeError: If there is a failure during the caching process (e.g., Redis issues).
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                _prefix = prefix or func.__name__

                key = self.get_cache_name(_prefix, *args, **kwargs)

                try:
                    cached_data = await self.get(key)
                except Exception as exc:
                    logger.error(f"Error during Redis get operation {exc!s}")
                    cached_data = None
                
                if cached_data is not None:
                    try:
                        return DataSerializer(cached_data).deserialized
                    except Exception as exc:
                        logger.error(str(exc))

                result = await func(*args, **kwargs)

                if isinstance(result, not_cache_on_type):
                    return result
                
                try:
                    set_data = DataSerializer(result).serialized
                except Exception as exc:
                    logger.error(str(exc))
                    return result

                try:
                    await self.set(key, set_data, ex=expiry)
                except Exception as e:
                    logger.error(f"Error during Redis set operation: {e!s}")

                return result

            return wrapper
        return decorator

    @staticmethod    
    def no_op_decorator(function: Callable) -> Callable:
        """
        Decorator that returns exac same function which gets in params. This function is used
        to improve DX in the code

        Params:
            func (Callable): the function which returns instantly
        
        Returns:
            (Callable): exac same function which is given
        """
        return function
    
    def cache_method(
        self,
        expiry: int = 15 * 60,
        prefix: Optional[str] = None,
        is_classmethod: bool = True,
        not_cache_on_type: Sequence[Type] | Type | Undefined = Undefined
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
            not_cache_on_type (Sequence[Type] | Type | Undefined): An optional parameter used to restinct
                                                                 cache when edge type comes as result

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
        
        cf_decorator = self.cache_function(expiry=expiry, 
                                           prefix=prefix, 
                                           not_cache_on_type=not_cache_on_type)
        clsm = is_classmethod and classmethod or self.no_op_decorator

        def decorator(func):
            
            @clsm
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:

                cf_decorator_resp = await cf_decorator(func)(*args, **kwargs)
                return cf_decorator_resp
            return wrapper
        
        return decorator
