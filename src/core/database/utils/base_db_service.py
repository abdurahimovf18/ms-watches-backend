from typing import Any, Sequence

from sqlalchemy.engine.row import RowMapping
from sqlalchemy import Column, Table

from pydantic import BaseModel as PydBaseModel

from src.core.utils.cache import cache
from .base_model import BaseModel


class BaseDbService:
    model = BaseModel

    @staticmethod
    def model_to_dict(model: BaseModel) -> dict:
        """
        Converts a model object to a dictionary.

        Args:
            model (BaseModel): The model object to convert.

        Returns:
            dict: A dictionary representation of the model.
        """
        return model.as_dict()

    @staticmethod
    def row_to_dict(row: RowMapping) -> dict:
        """
        Converts a SQLAlchemy RowMapping object to a dictionary.

        Args:
            row (RowMapping): The RowMapping object to convert.

        Returns:
            dict: A dictionary representation of the row.
        """
        return dict(row)

    @classmethod
    def rows_to_dict(cls, rows: Sequence[RowMapping]) -> tuple[dict]:
        fn = cls.row_to_dict
        return tuple(map(fn, rows))
    
    @classmethod


    @classmethod
    @cache
    def model_cols(cls, model: BaseModel | None = None, *args, **kwargs) -> tuple:
        """
        Retrieve columns for the associated model based on provided arguments.

        This method combines positional arguments and the keys of keyword arguments 
        to determine which columns to retrieve from the model. It utilizes the 
        `get_columns` method of the associated model (`cls.model`) to fetch the relevant 
        columns.

        Args:
            *args: Positional arguments representing column names.
            **kwargs: Keyword arguments whose keys represent column names (values are ignored).

        Returns:
            tuple: A tuple of column objects corresponding to the provided column names 
                (from positional arguments and keyword argument keys).

        Raises:
            AttributeError: If `cls.model` is not defined or does not implement `get_columns`.

        Example:
            >>> class UserService(BaseService):
            >>>     model = User  # SQLAlchemy model

            >>> # Retrieve columns using positional arguments
            >>> UserService.model_cols("id", "name")
            [User.id, User.name]

            >>> # Retrieve columns using keyword argument keys
            >>> UserService.model_cols(id=1, name="John")
            [User.id, User.name]

            >>> # Combine positional arguments and keyword argument keys
            >>> UserService.model_cols("id", email="john@example.com")
            [User.id, User.email]
        """
        model = model or cls.model
        fields = (*args, *kwargs.keys()) or None

        return model.get_columns(fields)

    @classmethod
    @cache
    def cols_from_pyd(cls, source: Any, schema: PydBaseModel) -> tuple[Column]:
        """
        Extracts SQLAlchemy columns based on a Pydantic schema from a model or table.

        This method dynamically maps the fields defined in the provided Pydantic model 
        to the corresponding SQLAlchemy columns in the given source (either a SQLAlchemy model 
        or a table). It is primarily used for selecting specific columns when constructing queries.

        Parameters:
            source (Any): 
                The SQLAlchemy model or table from which columns will be extracted.
            schema (PydBaseModel): 
                The Pydantic model whose field names will be matched with columns in the 
                source (SQLAlchemy model or table).

        Returns:
            tuple[Column]: 
                A tuple containing SQLAlchemy column objects that correspond to the fields 
                defined in the Pydantic schema.

        Raises:
            TypeError: 
                If the provided `schema` is not an instance of `PydBaseModel`.
            ValueError: 
                If the provided `source` is not a valid SQLAlchemy model or table.

        Notes:
            - This method does not raise exceptions if valid parameters are given.
            - Designed for flexibility, it supports working with both ORM models and tables 
            in SQLAlchemy.
            - It can be used in complex queries, including those involving joins and nested relationships.

        Example:
            ```python
            # Define SQLAlchemy models
            model1 = SomeSQLAlchemyModel
            model2 = AnotherSQLAlchemyModel

            # Define Pydantic schemas
            class PydResultsModel1(BaseModel):
                id: int
                name: str

            class PydResultsModel2(BaseModel):
                id: int
                related_field: str

            # Use cols_from_pyd in a query
            query = select(
                model1,
                model2
            ).join(
                model2, model1.id == model2.model1_id
            ).options(
                load_only(
                    *cls.cols_from_pyd(model1, PydResultsModel1)
                ),
                load_only(
                    *cls.cols_from_pyd(model2, PydResultsModel2)
                )
            )
            ```

        Advantages:
            - Avoids hardcoding column names, improving code maintainability.
            - Ensures compatibility between SQLAlchemy models/tables and Pydantic schemas.
            - Simplifies dynamic column selection in queries, especially when building APIs.

        Edge Cases:
            - If a field defined in the schema does not exist in the source, it will be silently skipped.
            - Ensure that both `source` and `schema` are correctly defined to prevent unexpected behavior.
        """
        
        if isinstance(source, Table):
            iter_obj = source.c
        elif hasattr(source, "__table__"):
            iter_obj = source.__table__.c
        else:
            raise ValueError("source must be a valid SQLAlchemy ORM model or table")
        
        keys = schema.model_fields.keys()
        return tuple(getattr(iter_obj, key) for key in keys if hasattr(iter_obj, key))
