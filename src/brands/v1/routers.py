from fastapi import APIRouter, Depends
from .services import router_services as services

from .schemas import brands

from src.users.dependencies import get_admin


router = APIRouter(prefix="/v1", tags=["V1"])


# @router.post("/create")
# async def brand_create(brand: BrandCreateSchema) -> BrandCreateResponseSchema:
#     resp = await services.create_brand(brand=brand)
#     return resp


@router.get("/top")
async def get_top_brands(params: brands.BrTpParamSchema = Depends()) -> list[brands.BrTpRespSchema]:
    resp = await services.get_top_brands(params=params)
    return resp

# @router.get("/images")
# async def get_brand_images( ):

