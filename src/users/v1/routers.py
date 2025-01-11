from fastapi import Depends, APIRouter, status

from .services import router_services as services
from .dependencies import get_current_user, get_admin


from .schemas import (UserLoginSchema, 
    UserRegisterSchema, UserRegisterResponseSchema,
    UserLoginResponseSchema, UserDbSchema)


router = APIRouter(prefix="/v1", tags=["V1"])


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegisterSchema) -> UserRegisterResponseSchema:
    response = await services.register_user(user=user)
    return response


@router.post("/access_token/", status_code=status.HTTP_200_OK)
async def get_access_token(user: UserLoginSchema) -> UserLoginResponseSchema:
    response = await services.login_user(user=user)
    return response


@router.get("/me/", status_code=status.HTTP_200_OK)
async def me(user: UserDbSchema = Depends(get_current_user)) -> UserDbSchema:
    return user
