from fastapi import APIRouter, status, Depends

from .services import router_services as services
from .schemas import router as rs

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/links")
async def get_social_links(params: rs.SlReParamSchema = Depends()) -> list[rs.SlReRespSchema]:
    resp = await services.get_social_links(params=params)
    return resp
