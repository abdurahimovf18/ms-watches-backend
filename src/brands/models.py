from sqlalchemy import (
    Integer, ForeignKey, String, Boolean, Enum
)

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.automap import get_model
from src.core.database.utils.base_model import BaseModel
from src.core.base_settings import DB_ID_TYPE
from .constants import BrandImageTypes


class BrandsModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    country_id: Mapped[int] = mapped_column(DB_ID_TYPE, ForeignKey("countries.id", ondelete="RESTRICT"))


class BrandImagesModel(BaseModel):
    brand_image_type: Mapped[BrandImageTypes] = mapped_column(Enum(BrandImageTypes), nullable=False)
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    brand_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False
    )


countries = get_model("countries")
country_images = get_model("country_images")


if countries is None:
    class CountriesModel: pass
else:
    class CountriesModel(BaseModel):
        __table__ = getattr(countries, "__table__")


if country_images is None:
    class CountryImagesModel: pass
else:
    class CountryImagesModel(BaseModel):
        if hasattr(country_images, "__table__"):
            __table__ = getattr(country_images, "__table__")
