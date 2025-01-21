from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError, NoResultFound
from loguru import logger

from .token_services import get_jwt_token, hash_password, verify_password

from . import db, cache


from ..schemas import users


async def register_user(params: users.UsReParamSchema) -> users.UsReRespSchema:
    params.password = hash_password(params.password)

    try:
        response: dict = await db.save_user(params=params)
    except IntegrityError as exc:
        logger.info(str(exc))
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")     
    except Exception as exc:
        logger.error(f"Error occured while registering user: {exc!s}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
    
    return users.UsReRespSchema(**response)


async def login_user(params: users.UsLgParamSchema) -> users.UsLgRespSchema:
    try:
        user_data: dict = await db.get_user_by_email(params=params)
    except NoResultFound:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email or Password is incorrect")
    except Exception as exc:
        logger.error(f"Error occurred while fetching user: {exc!s}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

    # Verify password
    if not verify_password(params.password, user_data["password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email or Password is incorrect")

    # Check if the user's account is active
    is_user_active = user_data.get("is_active")
    if not is_user_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is not active")
   
    # Prepare JWT token payload
    token_payload = {
        "sub": str(user_data.get("id"))
    }

    # Generate JWT token
    access_token = get_jwt_token(data=token_payload)

    if access_token is None:
        logger.error("Failed to generate JWT token")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return users.UsLgRespSchema(access_token=access_token)
