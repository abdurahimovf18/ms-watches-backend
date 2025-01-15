from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr

from src.core.base_settings import DB_ID_TYPE
from .utils.base_model import BaseModel

from src.users.models import UsersModel
from src.watches.models import WatchesModel
from src.watches.models import WatchImagesModel
from src.watches.models import WatchDescriptionsModel
from src.countries.models import CountriesModel
from src.brands.models import BrandsModel
from src.brands.models import BrandImagesModel
from src.tags.models import TagsModel
from src.collections.models import CollectionsModel


class BrandsToWatchesModel(BaseModel):
    brand_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("brands.id", ondelete="CASCADE")
    )

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

    # Relationships
    # brand: Mapped["BrandsModel"] = relationship(
    #     "BrandsModel", back_populates="watches"
    # )
    # watch: Mapped["WatchesModel"] = relationship(
    #     "WatchesModel", back_populates="brands"
    # )


class TagsToWatchesModel(BaseModel):
    tag_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

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

    # Relationships
    # watch: Mapped["WatchesModel"] = relationship(
    #     "WatchesModel", back_populates="tags"
    # )
    # tag: Mapped["TagsModel"] = relationship(
    #     "TagsModel", back_populates="watches"
    # )


class CollectionsToWatchesModel(BaseModel):
    collection_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("collections.id", ondelete="CASCADE")
    )

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
