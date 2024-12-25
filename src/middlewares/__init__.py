from fastapi import FastAPI

from .build_in_middlewares import register_cors_middleware


def register_middlewares(app: FastAPI) -> None:
    register_functions = [
        register_cors_middleware,
    ]

    for function in register_functions:
        function(app=app)
