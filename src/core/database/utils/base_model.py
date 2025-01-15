from datetime import datetime, timezone
from typing import Sequence

import re

from pydantic import BaseModel as PydBaseModel

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy import Integer, DateTime, func, inspect, Column

from sqlalchemy.orm.properties import MappedColumn

from src.core.base_settings import TIMEZONE
from src.core.utils.cache import cache

from ..database_set import default_metadata
from src.core.base_settings import DB_ID_TYPE


class PkField:
    """
    A base mixin class that provides an `id` primary key field.
    This class can be inherited to add the primary key field to models.
    """
    id = Column("id", DB_ID_TYPE, primary_key=True, unique=True)
    # `mapped_column` is used to define the SQLAlchemy column. Here, `Integer` is the column type
    # and the field is marked as the primary key and unique.


class TimeRegisterFields:
    """
    A mixin class that provides `created_at` and `updated_at` fields.
    These fields are typically used to track when a record was created and when it was last updated.
    """
    created_at = Column(
        "created_at",
        DateTime, 
        server_default=func.timezone(str(TIMEZONE), func.now())
    )
    # `created_at` field uses SQLAlchemy's `func.timezone('UTC', func.now())` to set the default value
    # to the current time in UTC. This ensures that when a record is created, it gets the correct UTC timestamp.

    updated_at = Column(
        "updated_at",
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
    __allow_unmapped__ = True

    metadata = default_metadata

    @staticmethod
    def get_table_name(name: str):
        """
        Dynamically generates the `__tablename__` for the model based on the class name.
        Converts the class name to snake_case and removes the "Model" suffix if present.
        For example:
            - `UserModel` becomes `user`
            - `WatchModel` becomes `watch`
            - `SomeOtherClass` becomes `some_other_class`

        Returns:
            str: The dynamically generated table name in snake_case format.
        """
        snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        # Remove "_model" suffix if present
        return snake_case_name.removesuffix("_model")
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Dynamically generates the `__tablename__` for the model based on the class name.
        Converts the class name to snake_case and removes the "Model" suffix if present.
        For example:
            - `UserModel` becomes `user`
            - `WatchModel` becomes `watch`
            - `SomeOtherClass` becomes `some_other_class`

        Returns:
            str: The dynamically generated table name in snake_case format.
        """

        name = cls.__name__

        # Convert CamelCase to snake_case
        return cls.get_table_name(name=name)

    @classmethod
    @cache
    def get_column_names(cls):
        """
        Retrieves the column names of the model by inspecting the class's columns.
        The result is cached for efficiency, avoiding repetitive inspections of the same model.

        Args:
            cls (type): The class object, automatically passed by SQLAlchemy.

        Returns:
            tuple: A tuple of column names for the model.
        """
        inspector = inspect(cls)  # Inspect the model to get information about its columns.
        return tuple(inspector.columns.keys())  # Return the tuple of column names.

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
    
    @classmethod
    @cache
    def get_columns(cls, fields: Sequence[str] | None = None) -> tuple:
        """
        Retrieve the database columns for the model class.

        This method uses SQLAlchemy's `inspect` to access the model's mapped columns. 
        If no specific fields are provided, it returns all columns defined in the model.
        If a tuple of field names is provided, it filters and returns only those columns
        that match the specified names.

        Args:
            fields (Sequence[str] | None): 
                An optional tuple of column names to filter. If `None`, all columns
                from the model are returned.

        Returns:
            tuple: 
                A tuple of SQLAlchemy column objects. If `fields` is provided, the tuple 
                contains only the columns matching the specified field names. Otherwise, 
                it includes all columns of the model.

        Example:
            >>> class User(Base):
            >>>     __tablename__ = "users"
            >>>     id = Column(Integer, primary_key=True)
            >>>     name = Column(String)
            >>>     email = Column(String)

            >>> # Retrieve all columns
            >>> User.get_columns()
            [User.id, User.name, User.email]

            >>> # Retrieve specific columns
            >>> User.get_columns(fields=["id", "name"])
            [User.id, User.name]
        """
        mapper = inspect(cls)

        if fields is None:
            return mapper.c.values()
        
        return tuple(val for key, val in mapper.c.items() if key in fields)
    
    @classmethod
    def get_orm_cols(cls):
        """
        Retrieves all ORM columns defined in the class and its base classes.

        This method traverses the method resolution order (MRO) of the class to collect
        all columns defined in the class and its ancestors. It looks for attributes that 
        are instances of `Column` and returns them as a list. This is useful for introspecting 
        the model's columns in a flexible way, including columns defined in base classes.

        Returns:
            list[Column]: A list of `Column` objects found in the class's MRO. These columns 
            represent the model's schema.
        
        Example:
            columns = MyModel.get_orm_cols()
            # Returns a list of Column objects defined in MyModel and its base classes
        """
        clses = cls.__mro__  # Get the method resolution order (MRO)

        resp = []

        for class_ in clses:
            for val in class_.__dict__.values():
                if isinstance(val, Column):
                    resp.append(val)

        return resp


    @classmethod
    @cache
    def cols_from_pyd(cls, pyd_model: PydBaseModel) -> tuple:
        """
        Retrieves columns from a Pydantic model's fields and maps them to the ORM columns.

        This method takes a Pydantic model (`pyd_model`) and uses its `model_fields` to extract 
        the corresponding ORM columns. It caches the result to improve performance when 
        dealing with repeated lookups. This is useful for dynamically converting Pydantic models 
        into SQLAlchemy columns, ensuring consistency between the schema definitions.

        Args:
            pyd_model (PydBaseModel): The Pydantic model from which the ORM columns are derived.
        
        Returns:
            tuple: A tuple of `Column` objects mapped from the Pydantic model's fields, 
            typically corresponding to the columns defined in the SQLAlchemy model.
        
        Example:
            pyd_model = MyPydanticModel
            columns = MyModel.cols_from_pyd(pyd_model)
            # Returns a tuple of Column objects corresponding to the model_fields of MyPydanticModel
        """
        return cls.get_columns(tuple(pyd_model.model_fields))
