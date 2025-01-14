from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Index

from src.core.database.utils.base_model import BaseModel


class CountriesModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    country_image: Mapped[str] = mapped_column(String(2048), )

    __table_args__ = (
        Index("countries_index_name", "name"),
    )
