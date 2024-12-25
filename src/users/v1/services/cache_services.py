from src.core.cache import cache


class UserCacheServices(cache.BaseCacheService):

    @cache.cache_method(expiry=15 * 60)
    async def get_user_by_id(cls, user_id: int) -> dict:
        db_resp = await cls.db_services.get_user_by_id(user_id=user_id)
        return db_resp
    