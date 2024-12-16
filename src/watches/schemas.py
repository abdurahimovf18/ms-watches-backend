from decimal import Decimal

from pydantic import BaseModel, Field
from src.utils.schemas import BaseDbSchema, BaseResponseSchema
from .constants import WatchStatus


class WatchRelationsSchema(BaseModel):
    watch_id: int


class DescriptionCreateSchema(WatchRelationsSchema):
    content: str


class ImageCreateSchema(WatchRelationsSchema):
    url: str


class LikeCreateSchema(WatchRelationsSchema):
    user_id: int


class LikeDbSchema(LikeCreateSchema, BaseDbSchema):
    pass


class ImageDbSchema(ImageCreateSchema, BaseDbSchema):
    pass


class DescriptionDbSchema(DescriptionCreateSchema, BaseDbSchema):
    pass


class WatchCreateSchema(BaseModel):
    name: str
    short_description: str
    descriptions: list[DescriptionCreateSchema] = Field(min_length=2)
    price: Decimal
    discount_percent: Decimal | None = Field(default=None)
    status: WatchStatus = Field(default=WatchStatus.INACTIVE)
    