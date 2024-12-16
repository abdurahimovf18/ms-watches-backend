from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey, DECIMAL, text, Enum

from src.utils.base_model import BaseModel
from .constants import WatchStatus


class WatchesModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    short_description: Mapped[str] = mapped_column(String(512), nullable=False)
    descriptions: Mapped[list["DescriptionsModel"]] = relationship(
        "DescriptionsModel", back_populates="watch", cascade="all, delete-orphan")

    images: Mapped[list["ImagesModel"]] = relationship(
        "ImagesModel", back_populates="watch", cascade="all, delete-orphan")
    
    price: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), nullable=False, 
                                                      server_default=text("0.00"))
    likes: Mapped[list["LikesModel"]] = relationship(
        "LikesModel", back_populates="watch", cascade="all, delete-orphan")
    
    status: Mapped[WatchStatus] = mapped_column(Enum(WatchStatus), server_default="INACTIVE")


class WatchRelatedModel(BaseModel):
    __abstract__ = True
    watch_id: Mapped[int] = mapped_column(Integer, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False)


class DescriptionsModel(WatchRelatedModel):
    content: Mapped[str] = mapped_column(Text, nullable=False)
    watch: Mapped[WatchesModel] = relationship("WatchesModel", back_populates="descriptions")


class ImagesModel(WatchRelatedModel):
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)  # Using String for URLs
    watch: Mapped[WatchesModel] = relationship("WatchesModel", back_populates="images")


class LikesModel(WatchRelatedModel):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user = relationship("UsersModel", back_populates="liked_watches")
    watch: Mapped[WatchesModel] = relationship("WatchesModel", back_populates="likes")
