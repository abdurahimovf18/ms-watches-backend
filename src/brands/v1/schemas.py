from fastapi import UploadFile
from pydantic import BaseModel

from src.utils.schemas import BaseDbSchema


class BrandCreateSchema(BaseModel):
    name: str


class BrandImageCreateSchema(BaseModel):
    image: UploadFile
    brand_id: int


class BrandDbSchema(BaseDbSchema, BrandCreateSchema):
    images: list[str]


class BrandCreateResponseSchema(BaseDbSchema, BrandCreateSchema):
    pass


# limit: int = 3, recent: bool = True, popular: bool = True,