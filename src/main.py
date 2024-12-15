from fastapi import FastAPI

from . import loader as l

from .auth.routers import router as auth_router


app = FastAPI(lifespan=l.lifespan)

app.include_router(router=auth_router)
