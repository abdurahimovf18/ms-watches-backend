from fastapi import FastAPI

from . import loader as l

from src.auth.models import UserModel


app = FastAPI(lifespan=l.lifespan)
