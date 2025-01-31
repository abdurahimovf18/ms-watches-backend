from fastapi import APIRouter, Depends
from .services import router_services as services

from .schemas import router as rs

from src.users.dependencies import get_admin


router = APIRouter(prefix="/v1", tags=["V1"])


@router.get("/top")
async def get_top_brands(params: rs.BrTpParamSchema = Depends()) -> list[rs.BrTpRespSchema]:
    resp = await services.get_top_brands(params=params)
    return resp


@router.get("/placeholder")
async def get_brand_placeholders(params: rs.BrPhParamSchema = Depends()) -> list[rs.BrPhRespSchema]:
    resp = await services.get_brand_placeholders(params=params)
    return resp
