from typing import Callable, Any, Awaitable
from functools import wraps

from loguru import logger

from .base_db_service import BaseDbService
from ..database_set import session_factory


class DbServices:
    DbService = BaseDbService

    @staticmethod
    def session_dependency(
        auto_commit: bool = False,
        auto_rollback: bool = True
        ) -> Callable:
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
                async with session_factory() as session:
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

    @staticmethod
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

    @staticmethod
    def no_op_decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """
        A no-operation decorator that does nothing but still allows async function behavior.
        """
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            return await func(*args, **kwargs)

        return wrapper

    def service(
        self,
        classmethod_: bool = True,
        provide_session: bool = True,
        auto_commit: bool = False,
        auto_rollback: bool = True,
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
        self_decorator = classmethod if classmethod_ else self.no_op_decorator

        # Apply session dependency if required
        session_decorator = self.session_dependency(auto_commit, auto_rollback) if provide_session else self.no_op_decorator

        def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
            """
            The actual service decorator that applies the appropriate decorators.
            """
            
            # Apply classmethod and session decorators
            @self_decorator
            @session_decorator
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            
            return wrapper
        
        return decorator


db_services = DbServices()