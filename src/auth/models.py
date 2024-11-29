from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.core.database.base_model import BaseModel


class UsersModel(BaseModel):

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)

