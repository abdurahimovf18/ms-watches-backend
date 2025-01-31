from datetime import datetime, timezone
from typing import Sequence, Any, Generator, Optional, Mapping

import re

from pydantic import BaseModel as PydBaseModel

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy import Integer, DateTime, func, inspect, Column

from sqlalchemy.orm.properties import MappedColumn

from sqlalchemy.sql.elements import Label

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


class BaseModelMethods:
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
        columns_string = ", ".join(f"{key}={getattr(self, key)}" for key in self.__mapper__.columns)
        return f"{type(self).__name__}({columns_string})"
    
    @classmethod
    @cache
    def get_orm_cols(cls, fields: Optional[Sequence[str]] = None) -> tuple[Column]:
        """
        Retrieve the database columns for the model class.

        This method uses SQLAlchemy's `inspect` to access the model's mapped columns. 
        If no specific fields are provided, it returns all columns defined in the model. 
        If a sequence of field names is provided, it filters and returns only those columns
        that match the specified names.

        Args:
            fields (Optional[Sequence[str]]): 
                A sequence of column names to filter the columns returned. If `None`, 
                all columns from the model are returned.

        Returns:
            tuple: 
                A tuple of SQLAlchemy `Column` objects. If `fields` is provided, the tuple 
                contains only the columns matching the specified field names. Otherwise, 
                it includes all columns of the model.

        Example:
            >>> class User(Base):
            >>>     __tablename__ = "users"
            >>>     id = Column(Integer, primary_key=True)
            >>>     name = Column(String)
            >>>     email = Column(String)

            >>> # Retrieve all columns
            >>> User.get_orm_cols()
            (User.id, User.name, User.email)

            >>> # Retrieve specific columns
            >>> User.get_orm_cols(fields=["id", "name"])
            (User.id, User.name)
        """
        keys = inspect(cls).c.keys()

        if fields is not None:
            fields = set(fields)
            keys = filter(lambda key: key in fields, keys)

        return tuple(getattr(cls, key) for key in keys)

    @classmethod
    @cache
    def get_aliased_cols(cls, 
                         source: Optional[Mapping] = None,
                         fields: Optional[Sequence[str]] = None, 
                         alias: Optional[dict[str, str]] = None) -> tuple[Column | Label]:
        """
        Retrieve aliased columns for the model class, allowing renaming of columns
        with an alias. This method uses SQLAlchemy's `inspect` to access the model's 
        columns and optionally applies an alias to specific columns.

        Args:
            source (Optional[Any]):
                A source if any other function or method is inherted from it.
            fields (Optional[Sequence[str]]): 
                A sequence of column names to filter the columns returned. If `None`, 
                all columns from the model are returned.
            alias (Optional[dict[str, str]]): 
                A dictionary mapping column names to aliases. If provided, the columns 
                matching the keys will have their names replaced with the corresponding alias.

        Returns:
            tuple: 
                A tuple of SQLAlchemy `Column` or `Label` objects. If `fields` is provided, 
                only the columns matching the specified field names will be returned. If 
                an alias is provided, columns will be returned with their labels.

        Example:
            >>> class User(Base):
            >>>     __tablename__ = "users"
            >>>     id = Column(Integer, primary_key=True)
            >>>     name = Column(String)
            >>>     email = Column(String)

            >>> # Retrieve all columns with aliases
            >>> User.get_aliased_cols(alias={"id": "user_id", "name": "user_name"})
            (Label('user_id', User.id), Label('user_name', User.name))

            >>> # Retrieve specific columns with aliases
            >>> User.get_aliased_cols(fields=["id", "name"], alias={"id": "user_id"})
            (Label('user_id', User.id), User.name)
        """
        source = source or inspect(cls).c
        item_gen = source.items()

        alias = alias or {}
        
        if fields is not None:
            item_gen = (d for d in item_gen if d[0] in fields)

        return tuple(cls.alias_generator(columns=item_gen, alias=alias))

    @staticmethod
    def alias_generator(columns: Generator[Column, None, None], 
                        alias: dict[str, str]) -> Generator[Column | Label, None, None]:
        """
        Generates aliased columns by applying aliases from the given dictionary to
        the columns.

        Args:
            columns (Generator[Column, None, None]): 
                A generator of SQLAlchemy `Column` objects to apply aliases to.
            alias (dict[str, str]): 
                A dictionary mapping column names to aliases. Columns whose names are in
                the dictionary will be given the corresponding alias.

        Yields:
            Column | Label: 
                Yields either the original column or an aliased column as a `Label` object.
        """
        for key, col in columns:
            if key in alias:
                yield col.label(alias[key])
            else:
                yield col

    @classmethod
    @cache
    def cols_from_pyd(cls, schema: PydBaseModel, alias: dict[str, str] | None = None) -> tuple[Column | Label]:
        """
        Maps Pydantic model fields to corresponding SQLAlchemy ORM columns.

        This method extracts the columns from a Pydantic model's fields using the model's 
        `model_fields` attribute and maps them to the appropriate SQLAlchemy columns. 
        The result is cached to optimize performance when performing repeated lookups. 
        It ensures that the fields defined in the Pydantic model align with the columns 
        in the corresponding SQLAlchemy model.

        Args:
            schema (PydBaseModel): 
                The Pydantic model whose fields will be mapped to SQLAlchemy columns.

        Returns:
            tuple[Column]: 
                A tuple of SQLAlchemy `Column` objects corresponding to the fields in the 
                provided Pydantic model.

        Example:
            ```python
            # Define a Pydantic model
            class MyPydanticModel(BaseModel):
                id: int
                name: str

            # Use cols_from_pyd to retrieve corresponding columns
            columns = MyModel.cols_from_pyd(MyPydanticModel)
            # Returns a tuple of Column objects corresponding to 'id' and 'name'
            ```

        Notes:
            - This method ensures consistency between Pydantic models and SQLAlchemy ORM models.
            - Caching improves efficiency by preventing repeated lookups of columns for the same Pydantic model.
            - Designed for dynamic conversion of Pydantic models to SQLAlchemy columns, simplifying the construction of queries.

        Edge Cases:
            - The `schema` argument should be a valid instance of a Pydantic model to avoid unexpected behavior.
        """
        return cls.get_aliased_cols(fields=set(schema.model_fields), alias=alias)

    @classmethod
    def set_automap_methods(cls, automap_cls: Any) -> None:

        for key, val in cls.__dict__.items():
            if hasattr(automap_cls, key):
                continue
            setattr(automap_cls, key, val)
    

class BaseModel(DeclarativeBase, PkField, TimeRegisterFields, BaseModelMethods):
    """
    A base model that combines primary key and time-tracking fields.
    This class is intended to be inherited by other model classes.
    
    It automatically adds common fields like `id`, `created_at`, and `updated_at`
    while providing methods for handling column names and converting instances to dictionaries.
    """

    __abstract__ = True
    __allow_unmapped__ = True

    metadata = default_metadata

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
    