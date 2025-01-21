from pydantic import BaseModel, Field


class BrPlaceholderSchema(BaseModel):
    name: str
    country_image_url: str | None = Field(default=None)


class BrTpParamSchema(BaseModel):
    limit: int = Field(default=10, gt=0)


class BrTpRespSchema(BrPlaceholderSchema):
    pass
