from sqlalchemy.engine.row import RowMapping
from typing import Any


class BaseDbService:
    model = ...

    @staticmethod
    def model_to_dict(model: Any) -> dict:
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
    def model_cols(cls, *args, **kwargs):
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
            list: A list of column objects corresponding to the provided column names 
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
        fields = (*args, *kwargs.keys()) or None
        return cls.model.get_columns(fields)
