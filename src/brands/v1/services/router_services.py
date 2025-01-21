from fastapi import status, HTTPException

from sqlalchemy.exc import IntegrityError
from loguru import logger

from . import db, cache
from ..schemas import brands, countries


# async def create_brand(brand: BrandCreateSchema) -> BrandCreateResponseSchema:
#     try:
#         resp: dict = await BrandDbServices.create_brand(new_brand=brand)
#     except IntegrityError as exc:
#         logger.info(str(exc))
#         raise HTTPException(status.HTTP_409_CONFLICT, detail=f'Brand "{brand.name}" already exists')    
    
#     return BrandCreateResponseSchema(**resp)


async def get_top_brands(params: brands.BrTpParamSchema) -> list[brands.BrTpRespSchema]:
    
    db_resp = await db.get_top_brands(params=params)

    return list(map(
            lambda value: brands.BrTpRespSchema(**value),
            db_resp
        ))