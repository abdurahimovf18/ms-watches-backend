from fastapi import Depends, APIRouter

from . import services
from .schemas import (UserLoginSchema, 
    UserRegisterSchema, UserRegisterResponseSchema,
    UserLoginResponseSchema, UserDbSchema)

from .utils import get_current_user


router = APIRouter(prefix="/auth")


@router.post("/signup/")
async def signup_view(user: UserRegisterSchema) -> UserRegisterResponseSchema:
    response = await services.register_user(user=user)
    return response


@router.post("/login/")
async def login_view(user: UserLoginSchema) -> UserLoginResponseSchema:
    response = await services.login_user(user=user)
    
    return response


@router.get("/me/")
async def me(user: UserDbSchema = Depends(get_current_user)) -> UserDbSchema:
    return user
