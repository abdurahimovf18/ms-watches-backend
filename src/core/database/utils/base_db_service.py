from typing import Any, Sequence

from sqlalchemy.engine.row import RowMapping
from sqlalchemy import Column, Table, inspect

from pydantic import BaseModel as PydBaseModel

from src.core.utils.cache import cache
from .base_model import BaseModel


class BaseDbService:
    model = BaseModel

    @staticmethod
    def model_to_dict(model: BaseModel) -> dict:
        """
        Converts a SQLAlchemy or Pydantic model object to a dictionary representation.
        
        Args:
            model (BaseModel): The model object to convert.

        Returns:
            dict: A dictionary representation of the model.

        Raises:
            AttributeError: If the model does not have a method `as_dict` or is not an instance 
                            of BaseModel.
        """
        if not hasattr(model, 'as_dict'):
            raise AttributeError(f"{model.__class__.__name__} does not have an 'as_dict' method.")
        return model.as_dict()

    @staticmethod
    def row_to_dict(row: RowMapping) -> dict:
        """
        Converts a SQLAlchemy RowMapping object to a dictionary.

        Args:
            row (RowMapping): The RowMapping object to convert.

        Returns:
            dict: A dictionary representation of the row.
        
        Notes:
            The keys in the dictionary will be converted to strings.
        """
        return {str(key): val for key, val in row.items()}

    @classmethod
    def rows_to_dict(cls, rows: Sequence[RowMapping]) -> tuple[dict]:
        """
        Converts a sequence of SQLAlchemy RowMapping objects into a tuple of dictionaries.

        Args:
            rows (Sequence[RowMapping]): A sequence of RowMapping objects to convert.

        Returns:
            tuple[dict]: A tuple of dictionary representations of the rows.

        Notes:
            This method applies the `row_to_dict` method to each element in the sequence using `map`.
        """
        fn = cls.row_to_dict
        return tuple(map(fn, rows))

    @classmethod
    @cache
    def model_cols(cls, model: BaseModel | None = None, *args, **kwargs) -> tuple:
        """
        Retrieves columns for the associated model based on provided arguments.

        Combines positional arguments and the keys of keyword arguments to determine which 
        columns to retrieve from the model. It uses the `get_columns` method of the associated model 
        (`cls.model`) to fetch the relevant columns. If no model is passed, it defaults to using 
        `cls.model`.

        Args:
            model (BaseModel, optional): The model from which to retrieve columns. Defaults to `cls.model`.
            *args: Positional arguments representing column names.
            **kwargs: Keyword arguments whose keys represent column names (values are ignored).

        Returns:
            tuple: A tuple of column objects corresponding to the provided column names 
                (from positional arguments and keyword argument keys).

        Raises:
            AttributeError: If `cls.model` is not defined or does not implement `get_columns`.
            TypeError: If `args` or `kwargs` contains invalid column names.

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

        if not hasattr(model, 'get_columns'):
            raise AttributeError(f"{model.__class__.__name__} does not implement 'get_columns'.")
        
        return model.get_columns(fields)

    @classmethod
    @cache
    def cols_from_pyd(cls, 
                    source: Any, 
                    schema: PydBaseModel, 
                    alias: dict[str | str] | None = None) -> tuple[Column]:
        """
        Extracts the SQLAlchemy columns corresponding to a Pydantic schema.

        This method dynamically maps the fields defined in the provided Pydantic schema 
        to the corresponding SQLAlchemy columns in the given source (either a SQLAlchemy model 
        or a table). It is primarily used for constructing queries by selecting specific columns 
        that match the Pydantic schema.

        Args:
            source (Any): The SQLAlchemy model or table from which the columns will be extracted. 
                        This can be a model class or a `Table` object.
            schema (PydBaseModel): The Pydantic model whose field names will be matched with 
                                    the columns in the source. The fields of the Pydantic model 
                                    should correspond to the column names in the SQLAlchemy model.
            alias (dict[str | str] | None): An optional dictionary mapping field names in the 
                                        Pydantic schema to their aliases in the SQLAlchemy query. 
                                        If `None`, no aliasing is applied.

        Returns:
            tuple[Column]: A tuple containing SQLAlchemy `Column` objects that correspond 
                            to the fields defined in the Pydantic schema.

        Raises:
            TypeError: If the `schema` is not an instance of `PydBaseModel`.
            ValueError: If the `source` is not a valid SQLAlchemy model or table.

        Example:
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

            # Use cols_from_pyd in a query to select specific columns
            query = select(
                model1,
                model2
            ).join(
                model2, model1.id == model2.model1_id
            ).options(
                load_only(
                    *cls.cols_from_pyd(model1, PydResultsModel1, alias={"id": "model_id"})
                ),
                load_only(
                    *cls.cols_from_pyd(model2, PydResultsModel2)
                )
            )
        """
        if not isinstance(schema, PydBaseModel):
            raise TypeError(f"Expected a Pydantic model instance, but got {type(schema)}.")
        
        if isinstance(source, Table):
            column_collection = source
        elif hasattr(source, "__table__"):
            column_collection = inspect(source)
        else:
            raise ValueError(f"Expected a valid SQLAlchemy model or table, but got {type(source)}.")
                
        return BaseModel.get_aliased_cols(column_collection.c, alias=alias)
