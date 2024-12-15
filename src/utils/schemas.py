from datetime import datetime
from pydantic import BaseModel


class BaseDbSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime


class BaseResponseSchema(BaseModel):
    ok: bool
    detail: str
    