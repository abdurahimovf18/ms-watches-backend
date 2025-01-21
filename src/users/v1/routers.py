from fastapi import Depends, APIRouter, status

from .services import router_services as services
from .dependencies import get_current_user, get_admin


from .schemas import users

router = APIRouter(prefix="/v1", tags=["V1"])


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def register_user(params: users.UsReParamSchema) -> users.UsReRespSchema:
    response = await services.register_user(params=params)
    return response


@router.post("/access_token/", status_code=status.HTTP_200_OK)
async def get_access_token(params: users.UsLgParamSchema) -> users.UsLgRespSchema:
    response = await services.login_user(params=params)
    return response


@router.get("/me/", status_code=status.HTTP_200_OK)
async def me(user: users.UsDbSchema = Depends(get_current_user)) -> users.UsDbSchema:
    return user
