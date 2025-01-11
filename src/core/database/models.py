from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.base_settings import DB_ID_TYPE

from src.users.models import UsersModel
from src.watches.models import WatchesModel
from src.watches.models import WatchImagesModel
from src.watches.models import WatchDescriptionsModel
from src.watches.models import WatchRelatedModel
from src.brands.models import BrandsModel
from src.brands.models import BrandImagesModel
from src.tags.models import TagsModel
from src.collections.models import CollectionsModel


class BrandsToWatchesModel(WatchRelatedModel):
    brand_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("brands.id", ondelete="CASCADE")
    )

    # Relationships
    # brand: Mapped["BrandsModel"] = relationship(
    #     "BrandsModel", back_populates="watches"
    # )
    # watch: Mapped["WatchesModel"] = relationship(
    #     "WatchesModel", back_populates="brands"
    # )


class TagsToWatchesModel(WatchRelatedModel):
    tag_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    # watch: Mapped["WatchesModel"] = relationship(
    #     "WatchesModel", back_populates="tags"
    # )
    # tag: Mapped["TagsModel"] = relationship(
    #     "TagsModel", back_populates="watches"
    # )


class CollectionsToWatchesModel(WatchRelatedModel):
    collection_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("collections.id", ondelete="CASCADE")
    )

    # watch: Mapped["WatchesModel"] = relationship(
    #     "WatchesModel", back_populates="collections"
    # ) 
    # collection: Mapped["CollectionsModel"] = relationship(
    #     "CollectionsModel", back_populates="watches"
    # )


class LikesModel(WatchRelatedModel):    
    user_id: Mapped[int] = mapped_column(
        DB_ID_TYPE, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    # user: Mapped["UsersModel"] = relationship("UsersModel", back_populates="liked_watches")
    # watch: Mapped["WatchesModel"] = relationship("WatchesModel", back_populates="liked_users")
