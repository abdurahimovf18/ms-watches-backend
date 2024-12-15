from datetime import datetime, timezone
from functools import lru_cache

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy import Integer, DateTime, func, inspect

from src.core.base_settings import TIMEZONE

from ..core.database.database_set import default_metadata


class PkField:
    """
    A base mixin class that provides an `id` primary key field.
    This class can be inherited to add the primary key field to models.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    # `mapped_column` is used to define the SQLAlchemy column. Here, `Integer` is the column type
    # and the field is marked as the primary key and unique.


class TimeRegisterFields:
    """
    A mixin class that provides `created_at` and `updated_at` fields.
    These fields are typically used to track when a record was created and when it was last updated.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.timezone(str(TIMEZONE), func.now())
    )
    # `created_at` field uses SQLAlchemy's `func.timezone('UTC', func.now())` to set the default value
    # to the current time in UTC. This ensures that when a record is created, it gets the correct UTC timestamp.

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.timezone(str(TIMEZONE), func.now()), 
        onupdate=lambda: datetime.now(timezone.utc)
    )
    # `updated_at` field is automatically set to the current time in UTC on insert
    # and updated with the current time in UTC when the record is modified.
    # The `onupdate` argument is a lambda function that ensures the field is updated with the current time on modifications.


class BaseModel(DeclarativeBase, PkField, TimeRegisterFields):
    """
    A base model that combines primary key and time-tracking fields.
    This class is intended to be inherited by other model classes.
    
    It automatically adds common fields like `id`, `created_at`, and `updated_at`
    while providing methods for handling column names and converting instances to dictionaries.
    """

    __abstract__ = True
    metadata = default_metadata
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Dynamically defines the `__tablename__` for the model based on the class name.
        It converts the class name to lowercase and removes the "Model" prefix if present.
        For example, a class `UserModel` will have the table name `user`.

        Args:
            cls (type): The class object, automatically passed by SQLAlchemy.

        Returns:
            str: The dynamically generated table name.
        """
        return cls.__name__.lower().removesuffix("model")
    
    @classmethod
    @lru_cache(maxsize=1)
    def get_column_names(cls):
        """
        Retrieves the column names of the model by inspecting the class's columns.
        The result is cached for efficiency, avoiding repetitive inspections of the same model.

        Args:
            cls (type): The class object, automatically passed by SQLAlchemy.

        Returns:
            list: A list of column names for the model.
        """
        inspector = inspect(cls)  # Inspect the model to get information about its columns.
        return list(inspector.columns.keys())  # Return the list of column names.

    def as_dict(self) -> dict:
        """
        Converts the model instance into a dictionary, mapping column names to their corresponding values.
        This is useful for serialization or returning a model as JSON-like data.

        Returns:
            dict: A dictionary where keys are column names and values are the corresponding values of the model.
        """
        return {key: getattr(self, key) for key in self.get_column_names()}
        # Iterate over the column names obtained from `get_column_names()` and use `getattr`
        # to retrieve the value of each attribute on the instance.

    def __repr__(self) -> str:
        columns_string = ", ".join(f"{key}={getattr(self, key)}" for key in self.get_column_names())
        return f"{type(self).__name__}({columns_string})"
    