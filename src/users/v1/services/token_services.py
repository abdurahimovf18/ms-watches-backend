from datetime import datetime
from typing import Optional, Dict, Any
import jwt
from loguru import logger
from ..settings import ENV_DATA
from src.core.base_settings import TIMEZONE
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12, 
    deprecated="auto" 
)

def get_jwt_token(data: Dict[str, Any]) -> Optional[str]:
    """
    Generates a JWT token with dynamic payload and customizable parameters.

    :param data: A dictionary of data to include in the token (user data, etc.)
    :return: Encoded JWT as a string, or None if encoding fails
    """
    if not ENV_DATA.SECRET_KEY or not ENV_DATA.JWT_ALGORITHM:
        logger.error("JWT configuration is missing required keys.")
        return None

    now = datetime.now(TIMEZONE)

    header = {
        "alg": ENV_DATA.JWT_ALGORITHM,
        "typ": "JWT",
    }

    payload = {
        "iss": ENV_DATA.ISSUER,
        "aud": ENV_DATA.AUDIENCE,
        "exp": (now + ENV_DATA.JWT_EXPIRE_TIME).timestamp(),
        "iat": now.timestamp(),
        "nbf": now.timestamp(),
    }
    
    payload.update(data)

    try:
        token = jwt.encode(
            headers=header,
            payload=payload,
            key=ENV_DATA.SECRET_KEY,
            algorithm=ENV_DATA.JWT_ALGORITHM
        )
        return token
    except jwt.PyJWTError as e:
        logger.error(f"Failed to encode JWT token: {e}")
        return None


def get_data_from_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes a JWT token and returns the data from the payload.

    :param token: The JWT token to decode
    :return: Decoded data from the token, or None if decoding fails
    """
    if not ENV_DATA.SECRET_KEY or not ENV_DATA.JWT_ALGORITHM:
        logger.error("JWT configuration is missing required keys.")
        return None

    try:
        decoded_data = jwt.decode(
            jwt=token,
            key=ENV_DATA.SECRET_KEY,
            algorithms=[ENV_DATA.JWT_ALGORITHM],
            audience=ENV_DATA.AUDIENCE,
            options={"require": ["exp", "iat", "nbf"]}
        )
        return dict(decoded_data)
    
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired.")
    except jwt.InvalidAudienceError:
        logger.warning("Invalid audience in JWT token.")
    except jwt.InvalidIssuerError:
        logger.warning("Invalid issuer in JWT token.")
    except jwt.PyJWTError as e:
        logger.error(f"Failed to decode JWT token: {e}")
    
    return None


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Handle invalid hash formats or other errors
        return False
    