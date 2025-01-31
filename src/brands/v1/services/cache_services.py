from typing import TypeAlias
from sqlalchemy.sql.elements import quoted_name

from src.core.cache import cache
from .db_services import BrandDbServices
from ..schemas import router as rs


Sequence: TypeAlias = list[dict] | tuple[dict]


class BrandCacheServices(cache.CacheService):
    db_services = BrandDbServices

    @cache.cache_method()
    async def get_top_brands(cls, params: rs.BrTpParamSchema) -> Sequence:
        return await cls.db_services.get_top_brands(params=params)
    
    @cache.cache_method()
    async def get_brand_placeholders(cls, params: rs.BrPhParamSchema) -> Sequence:
        return await cls.db_services.get_brand_placeholders(params=params)
        
