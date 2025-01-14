from fastapi import FastAPI

from . import loader as l

from .middlewares import register_middlewares
import src.core.database.models


app = FastAPI(lifespan=l.lifespan)

register_middlewares(app=app)