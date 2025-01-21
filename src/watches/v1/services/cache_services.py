
from src.core.cache import cache
from .db_services import WatchDbServices as db
from ..schemas import watch


class WatchCacheServices(cache.CacheService):
    db_services = db

    @cache.cache_method()
    async def get_featured_watches(cls, params: watch.WaFeParamSchema) -> tuple[dict] | list[dict]:
        return await cls.db_services.get_featured_watches(params=params)


    @cache.cache_method()
    async def get_top_weekly_watches(cls, params: watch.WaFeParamSchema) -> dict:
        return await cls.db_services.get_top_weekly_watches(params=params)
    
    @cache.cache_method()
    async def get_new_arrivals(cls, params: watch.WaNaParamSchema) -> tuple[dict] | list[dict]:
        return await cls.db_services.get_new_arrivals(params=params)
    