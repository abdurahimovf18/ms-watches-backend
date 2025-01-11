from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, Index, Boolean

from src.core.database.utils.base_model import BaseModel


class UsersModel(BaseModel):

    NAME_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 25
    EMAIL_MAX_LENGTH = 255
    PASSWORD_MAX_LENGTH = 255

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    first_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(PHONE_MAX_LENGTH), 
        nullable=False, 
        unique=True, 
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(EMAIL_MAX_LENGTH), 
        nullable=False, 
        unique=True, 
        index=True
    )
    password: Mapped[str] = mapped_column(
        String(PASSWORD_MAX_LENGTH), 
        nullable=False
    )

    # liked_watches: Mapped[list["LikesModel"]] = relationship(
    #     "LikesModel", back_populates="user"
    # )

    __table_args__ = (
        UniqueConstraint('email', name='uq_email'),
        UniqueConstraint('phone_number', name='uq_phone_number'),
        Index('ix_phone_number', 'phone_number'),
        Index('ix_email', 'email'),
    )
