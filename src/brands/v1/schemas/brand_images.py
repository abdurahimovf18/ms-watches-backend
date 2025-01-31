from pydantic import BaseModel


class BrPhRespSchema(BaseModel):
    brand_image_url: str
