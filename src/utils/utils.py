from typing import Iterable, Mapping, Type
from pydantic import BaseModel as PydBaseModel


def compile_all(data: Iterable[Mapping], schema: Type[PydBaseModel]) -> list[PydBaseModel]:
    """Compiles all items in data into instances of the given schema."""
    return [schema(**element) for element in data]


def compile_one(data: Mapping, schema: Type[PydBaseModel]) -> PydBaseModel:
    """Compiles a single item into an instance of the given schema."""
    return schema(**data)
