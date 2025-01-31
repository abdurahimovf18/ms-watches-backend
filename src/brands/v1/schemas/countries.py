from pydantic import BaseModel, Field


class BrTpRespSchema(BaseModel):
    country_image_url: str | None = Field(default=None)
