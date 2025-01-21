from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.utils.schemas import BaseCreateSchema, BaseDbSchema


class UsLgParamSchema(BaseModel):
    email: EmailStr
    password: str


class UsLgDbRespSchema(BaseModel):
    id: int = Field(gt=0)
    password: str
    is_active: bool


class UsReParamSchema(UsLgParamSchema):
    phone_number: PhoneNumber
    first_name: str
    last_name: str


class UsDbSchema(UsReParamSchema, BaseDbSchema):
    is_active: bool
    is_superuser: bool
    is_staff: bool


class UsReRespSchema(BaseCreateSchema):
    email: EmailStr
    first_name: str
    last_name: str


class UsLgRespSchema(BaseModel):
    access_token: str


class UsPkParamSchema(BaseModel):
    user_id: int = Field(gt=0)


class UsPkRespSchema(UsDbSchema):
    pass
