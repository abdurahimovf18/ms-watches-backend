from src.core.cache import cache

from .db_services import SocialLinksDbServices
from ..schemas import router as rs


class SocialLinksCacheServices(cache.CacheService):
    db_services = SocialLinksDbServices

    @cache.cache_method()
    async def get_social_links(cls, params: rs.SlReParamSchema) -> list[dict] | tuple[dict]:
        return await cls.db_services.get_social_links(params=params)
    