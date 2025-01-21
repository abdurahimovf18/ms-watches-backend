from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, declared_attr
from sqlalchemy import String, Text, ForeignKey, DECIMAL, text, Enum, CheckConstraint, Index
from src.core.database.utils.base_model import BaseModel
from src.core.base_settings import DB_ID_TYPE
from .constants import WatchStatus, WatchImageType



class WatchesModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    short_description: Mapped[str] = mapped_column(String(512), nullable=False)
    
    price: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 2), nullable=False, server_default=text("0.00")
    )
    status: Mapped[WatchStatus] = mapped_column(Enum(WatchStatus), server_default="INACTIVE")

    # Relationships
    descriptions: Mapped[list] = relationship(
        "WatchDescriptionsModel", back_populates="watch"
    )

    # liked_users: Mapped[list] = relationship(
    #     "LikesModel", back_populates="watch"
    # )

    # brands: Mapped[list] = relationship(
    #     "BrandsToWatchesModel", back_populates="watch"
    # )
    # tags: Mapped[list] = relationship(
    #     "TagsToWatchesModel", back_populates="watch"
    # )
    # collections: Mapped[list] = relationship(
    #     "CollectionsToWatchesModel", back_populates="watch"
    # )

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_positive_price"),
        CheckConstraint(
            "discount_percent >= 0 AND discount_percent <= 100",
            name="check_valid_discount_percent"
        ),
    )

    # Validations
    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price must be greater than or equal to 0.")
        return price

    @validates("discount_percent")
    def validate_discount_percent(self, key, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100.")
        return discount_percent

    @validates("name")
    def validate_name(self, key, name):
        if not name.strip():
            raise ValueError("Name cannot be empty or whitespace.")
        return name

    @validates("short_description")
    def validate_short_description(self, key, short_description):
        if len(short_description) > 512:
            raise ValueError("Short description exceeds the 512 character limit.")
        return short_description

        
class WatchDescriptionsModel(BaseModel):
    content: Mapped[str] = mapped_column(Text, nullable=False)
    watch: Mapped["WatchesModel"] = relationship("WatchesModel", back_populates="descriptions")

    watch_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False
    )

    @declared_attr
    def __table_args__(cls):
        args = (
            Index(f'{cls.__tablename__}_index_watch_id', 'watch_id'),
        )

        parent_args = getattr(super(), "__table_args__", ()) or ()
        return parent_args + args


class WatchImagesModel(BaseModel):
    watch_image_type: Mapped[WatchImageType] = mapped_column(Enum(WatchImageType), nullable=False, default="DEFAULT")
    watch_image_url: Mapped[str] = mapped_column(String(2048), nullable=False)

    @declared_attr
    def __table_args__(cls):
        args = (
            Index(f"{cls.__tablename__}_image_type_index", "image_type"),
            Index(f"{cls.__tablename__}_composite_index", "watch_id", "image_type"),
        )
        parent_args = getattr(super(), "__table_args__", ()) or ()
        return parent_args + args
    
    watch_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("watches.id", ondelete="CASCADE"), nullable=False
    )

    @declared_attr
    def __table_args__(cls):
        args = (
            Index(f'{cls.__tablename__}_index_watch_id', 'watch_id'),
        )

        parent_args = getattr(super(), "__table_args__", ()) or ()
        return parent_args + args
