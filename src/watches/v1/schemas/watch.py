from decimal import Decimal

from pydantic import BaseModel, Field


class WaSaveDbRespSchema(BaseModel):
    watch_id: int
    name: str
    short_description: str
    price: Decimal
    discount_percent: Decimal
    image_url: str


class WaFeParamSchema(BaseModel):
    limit: int = Field(default=4, gt=0)


class WaFeRespSchema(WaSaveDbRespSchema):
    pass


class WaTwParamSchema(BaseModel):
    pass


class WaTwRespSchema(BaseModel):
    watch_id: int
    image_url: str
    name: str
    

class WaNaParamSchema(BaseModel):
    limit: int = Field(gt=0, default=4)


class WaNaRespSchema(WaSaveDbRespSchema):
    pass
