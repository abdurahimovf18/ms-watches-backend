from pydantic import BaseModel
from src.utils.schemas import BaseDbSchema


class WIContentSchema(BaseModel):
    watch_image_url: str


class WISchema(WIContentSchema):
    watch_id: int


class WIDbSchema(BaseDbSchema, WISchema):
    pass
