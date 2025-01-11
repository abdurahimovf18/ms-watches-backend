from datetime import datetime
from pydantic import BaseModel


class BaseCreateSchema(BaseModel):
    created_at: datetime


class BaseUpdateSchema(BaseModel):
    updated_at: datetime


class BaseTimeSchema(BaseUpdateSchema, BaseCreateSchema):
    pass


class BaseIdSchema(BaseModel):
    id: int


class BaseDbSchema(BaseTimeSchema, BaseIdSchema):
    pass
