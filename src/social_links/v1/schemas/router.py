from pydantic import BaseModel, Field

from . import social_links


class SlReParamSchema(BaseModel):
    limit: int = Field(default=-1, ge=-1)


class SlReRespSchema(social_links.SlReRespSchema):
    pass
