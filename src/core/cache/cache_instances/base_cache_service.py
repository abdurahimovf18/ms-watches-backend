from .base_instance import CacheInstanceAbs


class BaseCacheService:
    """
    A base class for caching services that provides shared functionality for managing
    cache instances and interacting with the cache in a modular way. This class can be
    inherited by specific service classes to implement caching functionality for different
    data models.

    Attributes:
        db_services (BaseService): A placeholder for the database service class that
                                    this cache service interacts with.
        c (CacheInstanceAbs): A placeholder for the cache instance used to store and
                              retrieve data.

    Methods:
        set_cache_instance(cls, instance: CacheInstanceAbs) -> None:
            Sets the cache instance to be used by the cache service class.
    """

    db_services = ...
    c: CacheInstanceAbs

    @classmethod
    def set_db_services(cls, db_serivices):
        cls.db_services = db_serivices

    @classmethod
    def set_cache_instance(cls, instance: CacheInstanceAbs) -> None:
        """
        Sets the cache instance for the cache service class.

        This method allows you to define the cache instance (e.g., Redis, Memcached)
        that will be used by the cache service to store and retrieve data. It ensures
        that the cache instance is configured before using any caching operations.

        Args:
            instance (CacheInstanceAbs): The cache instance to be used for the service.
        
        Returns:
            None
        """
        cls.c = instance
