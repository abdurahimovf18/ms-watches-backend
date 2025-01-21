from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Index, Enum

from src.core.database.utils.base_model import BaseModel
from src.core.base_settings import DB_ID_TYPE
from .constants import CountryImageTypes


class CountriesModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    
    __table_args__ = (
        Index("countries_index_name", "name"),
    )


class CountryImagesModel(BaseModel):
    country_id: Mapped[int] = mapped_column(DB_ID_TYPE, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)

    country_image_type: Mapped[CountryImageTypes] = mapped_column(Enum(CountryImageTypes))
    country_image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
