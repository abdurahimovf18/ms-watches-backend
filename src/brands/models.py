from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.utils.base_model import BaseModel


class BrandsModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # images = relationship("BrandImagesModel", back_populates="brand", cascade="all, delete-orphan")
    
    # associated_watches: Mapped[list["BrandsToWatchesModel"]] = relationship(
    #     "BrandsToWatchesModel", back_populates="brand", cascade="all, delete-orphan"
    # )


class BrandImagesModel(BaseModel):
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    brand_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False
    )

    # brand: Mapped["BrandsModel"] = relationship("BrandsModel", back_populates="images")
