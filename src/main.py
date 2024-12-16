from fastapi import FastAPI

from . import loader as l


app = FastAPI(lifespan=l.lifespan)

