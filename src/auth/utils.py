from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .services import get_data_from_jwt
from .services import UsersService

from .schemas import UserDbSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDbSchema:
    """
    Dependency to get the current user by verifying the JWT token.
    """

    payload = get_data_from_jwt(token=token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token is invalid")

    user_id: int = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await UsersService.get_user_by_id(user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserDbSchema(**user)
