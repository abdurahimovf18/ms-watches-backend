from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.utils.schemas import BaseDbSchema, BaseResponseSchema


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    phone_number: PhoneNumber
    first_name: str
    last_name: str


class UserDbSchema(UserRegisterSchema, BaseDbSchema):
    is_active: bool
    is_superuser: bool
    is_staff: bool


class UserRegisterResponseSchema(BaseResponseSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    token: str
    ok: bool
    