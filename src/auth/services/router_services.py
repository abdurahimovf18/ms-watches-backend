from fastapi import HTTPException, status

from loguru import logger

from .token_services import get_jwt_token, get_data_from_jwt, hash_password, verify_password

from .db_services import UsersService

from ..schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    UserLoginResponseSchema,
    UserRegisterResponseSchema,
    )


async def register_user(user: UserRegisterSchema) -> UserRegisterResponseSchema:
    user.password = hash_password(user.password)

    try:
        response = await UsersService.save_user(new_user=user)
    except Exception as exc:
        logger.critical(str(exc))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

    if response: 
        return UserRegisterResponseSchema(ok=True, detail="User created successfully")

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


async def login_user(user: UserLoginSchema) -> UserLoginResponseSchema:
    
    user_data = await UsersService.get_user_by_email(email=user.email)

    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Password is incorrect")
    
    is_password_valid= verify_password(user.password, user_data["password"])

    if not is_password_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Password is incorrect")

    token_data = {
        "sub": user_data["id"]
    }

    access_token = get_jwt_token(data=token_data)

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

    resp = UserLoginResponseSchema(token=access_token, ok=True)
    
    return resp
