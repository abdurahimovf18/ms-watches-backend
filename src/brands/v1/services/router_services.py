from fastapi import status, HTTPException

from .db_services import BrandServices
from ..schemas import BrandCreateSchema, BrandCreateResponseSchema


async def create_brand(brand: BrandCreateSchema) -> BrandCreateResponseSchema:
    resp = await BrandServices.create_brand(new_brand=brand)


    return BrandCreateResponseSchema(resp)
