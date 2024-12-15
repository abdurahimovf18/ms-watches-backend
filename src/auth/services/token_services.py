
from datetime import datetime
from authlib.jose import jwt
from authlib.jose.errors import InvalidTokenError
from loguru import logger
from ..settings import ENV_DATA
from src.core.base_settings import TIMEZONE
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12, 
    deprecated="auto" 
)


def get_jwt_token(data: dict) -> str | None:
    """
    Generates a JWT token with dynamic payload and customizable parameters.

    :param data: A dictionary of data to include in the token (user data, etc.)
    :return: Encoded JWT as a string, or None if encoding fails
    """
    
    payload_data = data.copy()

    now = datetime.now(TIMEZONE)
    
    header = {
        'alg': ENV_DATA.JWT_ALGORITHM,
    }

    payload = {
        'iss': ENV_DATA.ISSUER,
        'aud': ENV_DATA.AUDIENCE,
        'exp': (now + ENV_DATA.JWT_EXPIRE_TIME).timestamp(),
        'iat': now.timestamp(),
        'nbf': now.timestamp(),
    }

    payload.update(payload_data)

    try:
        token = jwt.encode(header, payload, ENV_DATA.SECRET_KEY)
        return token.decode()
    except Exception as e:
        logger.error(f"JWT encoding error: {e!s}")
        return None


def get_data_from_jwt(token: str) -> dict | None:
    """
    Decodes a JWT token and returns the data from the payload.

    :param token: The JWT token to decode
    :return: Decoded data from the token, or None if decoding fails
    """
    try:
        data = jwt.decode(token, ENV_DATA.SECRET_KEY)
        data.validate(now=datetime.now(TIMEZONE).timestamp())
        return dict(data)
    
    except InvalidTokenError:
        return None
    
    except Exception as e:
        logger.error(f"JWT decoding error: {str(e)}")
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
    