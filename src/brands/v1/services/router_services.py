from fastapi import status, HTTPException

from sqlalchemy.exc import IntegrityError
from loguru import logger

from .db_services import BrandDbServices
from ..schemas import BrandCreateSchema, BrandCreateResponseSchema


async def create_brand(brand: BrandCreateSchema) -> BrandCreateResponseSchema:
    try:
        resp: dict = await BrandDbServices.create_brand(new_brand=brand)
    except IntegrityError as exc:
        logger.info(str(exc))
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f'Brand "{brand.name}" already exists')    
    
    return BrandCreateResponseSchema(**resp)
