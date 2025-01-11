from fastapi import UploadFile
from pydantic import BaseModel

from src.utils.schemas import BaseDbSchema, BaseCreateSchema


class BrandCreateSchema(BaseModel):
    name: str


class BrandImageCreateSchema(BaseModel):
    image: UploadFile
    brand_id: int


class BrandDbSchema(BaseDbSchema, BrandCreateSchema):
    images: list[str]


class BrandCreateResponseSchema(BrandCreateSchema, BaseCreateSchema):
    pass
