from sqlalchemy import (
    Integer, ForeignKey, String, Boolean
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.database_set import engine
from src.core.database.utils.base_model import BaseModel
from .constants import BrandImageTypes


class BrandsModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)



class BrandImagesModel(BaseModel):
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    brand_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False
    )
