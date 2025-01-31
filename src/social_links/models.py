from sqlalchemy import String, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_settings import DB_ID_TYPE
from src.core.database.utils.base_model import BaseModel



class SocialLinksModel(BaseModel):
    platform_name: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    social_link: Mapped[str] = mapped_column(String(2048))
    social_username: Mapped[str] = mapped_column(String(512))

    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    is_deleted: Mapped[str] = mapped_column(Boolean, server_default=text("false"))

    added_by: Mapped[int] = mapped_column(DB_ID_TYPE, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
