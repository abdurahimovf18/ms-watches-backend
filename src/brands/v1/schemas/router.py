from pydantic import BaseModel, Field

from . import brands
from . import countries
from . import brand_images


class BrTpRespSchema(brands.BrTpRespSchema, countries.BrTpRespSchema):
    pass


class BrTpParamSchema(BaseModel):
    limit: int = Field(default=10, gt=0)


class BrPhRespSchema(brands.BrPhRespSchema, brand_images.BrPhRespSchema):
    pass


class BrPhParamSchema(BaseModel):
    limit: int = Field(default=10, gt=0)
    