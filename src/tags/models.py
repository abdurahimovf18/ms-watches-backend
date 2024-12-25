from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.database.utils.base_model import BaseModel


class TagsModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # associated_watches: Mapped[list["TagsToWatchesModel"]] = relationship(
    #     "TagsToWatchesModel", back_populates="tag", cascade="all, delete-orphan"
    # )
    