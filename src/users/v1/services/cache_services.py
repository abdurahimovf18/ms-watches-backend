from src.core.cache import cache
from .db_services import UserDbServices


class UserCacheServices(cache.CacheService):

    db_services = UserDbServices

    @cache.cache_method(expiry=15 * 60, not_cache_on_type=None)
    async def get_user_by_id(cls, user_id: int) -> dict:
        db_resp = await cls.db_services.get_user_by_id(user_id=user_id)
        return db_resp
    