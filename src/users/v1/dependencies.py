from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .services.token_services import get_data_from_jwt
from .services import UserCacheServices
from .schemas import UserDbSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDbSchema:
    """
    Dependency to retrieve the current authenticated user.

    Verifies the JWT token, extracts the user ID, and fetches the user 
    from the database or cache. Raises HTTP exceptions for invalid tokens or users.

    :param token: The JWT token extracted from the Authorization header.
    :return: A UserDbSchema object representing the authenticated user.
    :raises HTTPException: If the token is invalid or the user is not found.
    """
    # Decode JWT token to extract payload
    payload = get_data_from_jwt(token=token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    # Extract user ID from token payload
    user_id: int = int(payload.get("sub"))

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user ID in token",
        )

    # Retrieve the user from cache or database
    user = await UserCacheServices.get_user_by_id(user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    user = UserDbSchema(**user)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User's account is not active"
        )

    return user


async def get_admin(user: UserDbSchema = Depends(get_current_user)) -> UserDbSchema:
    """
    Retrieve the current authenticated user and verify if the user is an admin.

    This dependency function checks whether the authenticated user has admin privileges
    (i.e., if the user is a superuser). If the user is not a superuser, an HTTP 403 
    Forbidden error is raised, indicating that the user does not have permission to access 
    the requested resource.

    Args:
        user (UserDbSchema): The currently authenticated user, retrieved from the `get_current_user` dependency.

    Returns:
        UserDbSchema: The authenticated user object, if the user is a superuser.

    Raises:
        HTTPException: If the user is not a superuser, with a 403 Forbidden status code.
    """
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    
    return user

