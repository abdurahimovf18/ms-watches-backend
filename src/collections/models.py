from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.utils.base_model import BaseModel


class CollectionsModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    # associated_watches = relationship(
    #     "CollectionsToWatchesModel", back_populates="collection", cascade="all, delete-orphan"
    # )
