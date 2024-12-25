from decimal import Decimal

from pydantic import BaseModel, Field
from src.utils.schemas import BaseDbSchema
from .constants import WatchStatus


class WatchRelationsSchema(BaseModel):
    watch_id: int


class DescriptionWatchDeclaretionCreateSchema(BaseModel):
    content: str


class DescriptionCreateSchema(WatchRelationsSchema, DescriptionWatchDeclaretionCreateSchema):
    pass


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
    descriptions: list[DescriptionWatchDeclaretionCreateSchema] = Field(min_length=2)
    price: Decimal
    discount_percent: Decimal | None = Field(default=None)
    status: WatchStatus = Field(default=WatchStatus.INACTIVE)


class WatchDbSchema(WatchCreateSchema, BaseDbSchema):
    pass


class WatchCreateResponseSchema(BaseModel):
    pass
