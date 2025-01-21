from src.core.cache import cache
from .db_services import BrandDbServices


class BrandCacheServices(cache.CacheService):
    db_services = BrandDbServices
