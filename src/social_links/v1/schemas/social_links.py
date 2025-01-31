from pydantic import BaseModel


class SlReRespSchema(BaseModel):
    platform_name: str
    social_link: str
    social_username: str
