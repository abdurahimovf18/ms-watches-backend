from fastapi import APIRouter
from . import services

from .schemas import BrandCreateSchema, BrandCreateResponseSchema

from src.users.dependencies import get_admin


router = APIRouter(prefix="/v1", tags=["V1"])


@router.post("/create")
async def brand_create(brand: BrandCreateSchema) -> BrandCreateResponseSchema:
    resp = await services.create_brand(brand=brand)
    return resp



# @router.get("/images")
# async def get_brand_images( ):

