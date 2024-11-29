from functools import wraps
from typing import Callable, Any, Awaitable

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import RowMapping

from sqlalchemy import select

from .database_set import session_factory
from .base_model import BaseModel


def session_dependency(
        auto_commit: bool = False,
        auto_rollback: bool = True) -> Callable:
    """
    A decorator to manage database session lifecycle in async functions.
    
    This decorator ensures that a session is created and injected into the
    decorated function's kwargs, handles automatic commit of changes, and
    manages exception handling, including session rollback in case of errors.

    Args:
        auto_commit (bool): If True, the session will be committed automatically
                             after the function executes. Default is False.
        auto_rollback (bool): If True, the session will be rolled back in case
                               of an exception. Default is True.

    Returns:
        Callable: A wrapped version of the original function that includes session
                  management.
    """
    
    def decorator(func) -> Callable:
        """
        The decorator that wraps the original function, injecting a session
        and handling commit or rollback behavior.
        
        Args:
            func (Callable): The original function to be wrapped.

        Returns:
            Callable: A wrapper function that includes session handling logic.
        """
        
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            """
            The wrapper function that manages the database session, performs
            automatic commit if needed, and handles rollback in case of exceptions.

            Args:
                *args: Positional arguments passed to the original function.
                **kwargs: Keyword arguments passed to the original function, 
                          including the database session.

            Returns:
                Any: The result of the decorated function, after session management.
            """
            # Open a session and ensure it is closed after the function execution
            async with session_factory.begin() as session:
                try:
                    # Inject the session into the function's keyword arguments
                    kwargs["session"] = session

                    # Call the decorated function with the session and other arguments
                    response = await func(*args, **kwargs)

                    # Commit the transaction if auto_commit is set to True
                    if auto_commit:
                        await session.commit()
                    
                    return response

                except Exception as exc:
                    # Rollback the session on error if auto_rollback is True
                    if auto_rollback:
                        await session.rollback()  # Ensures session rollback on error

                    # Re-raise the exception after rollback
                    raise exc

        return wrapper

    return decorator


def exception_decorator(func: Callable) -> Callable:
    """
    A decorator to catch and log any exceptions that occur during the 
    execution of the decorated asynchronous function.

    Args:
        func (Callable): The original function to be wrapped.

    Returns:
        Callable: A wrapper function that logs any exceptions.
    """
    
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            # Execute the function and pass the arguments
            return await func(*args, **kwargs)
        except Exception as exc:
            # Catch and log the exception using loguru
            logger.exception(f"An error occurred in {func.__name__}: {exc}")
            raise exc  # Re-raise the exception after logging it

    return wrapper



def no_op_decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """
    A no-operation decorator that does nothing but still allows async function behavior.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        return await func(*args, **kwargs)

    return wrapper


def service_decorator(
    classmethod_: bool = True,
    provide_session: bool = True,
    auto_commit: bool = False,
    auto_rollback: bool = True
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """
    A decorator to add service functionality to methods, with conditional session 
    handling, classmethod behavior, and transaction management (commit/rollback).

    Args:
        classmethod_ (bool): Whether to treat the method as a classmethod. Defaults to True.
        provide_session (bool): Whether to inject the session dependency. Defaults to True.
        auto_commit (bool): Whether to commit the session automatically. Defaults to False.
        auto_rollback (bool): Whether to automatically rollback the session on error. Defaults to True.

    Returns:
        Callable: A decorator that applies classmethod and session functionality to the decorated method.
    """

    # Apply classmethod decorator if required
    cls_decorator = classmethod if classmethod_ else no_op_decorator

    # Apply session dependency if required
    session_decorator = session_dependency(auto_commit, auto_rollback) if provide_session else no_op_decorator

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """
        The actual service decorator that applies the appropriate decorators.
        """
        
        # Apply classmethod and session decorators
        @cls_decorator
        @wraps(func)
        @session_decorator
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


class BaseService:
    model = BaseModel

    @service_decorator(auto_commit=True)
    async def get_object_by_id(cls, object_id: int, session: AsyncSession) -> dict:
        """
        Retrieves an object by its ID from the database.

        Args:
            cls: The class that inherits from BaseService.
            object_id (int): The ID of the object to retrieve.
            session (AsyncSession): The database session to use for the query.

        Returns:
            dict: A dictionary representation of the object, or an empty dictionary if not found.
        """
        query = select(cls.model).filter_by(id=object_id)
        db_response = await session.execute(query)

        if (obj := db_response.scalars().one_or_none()) is None:
            return {}
        else:
            return cls.model_to_dict(obj)

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
