from pydantic import BaseModel, Field


class BrTpRespSchema(BaseModel):
    id: int
    name: str


class BrPhRespSchema(BaseModel):
    id: int
    name: str
