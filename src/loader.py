from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

import src.core.log
from .auth.routers import router as auth_router
from .watches.routers import router as watches_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.include_router(router=watches_router)
    app.include_router(router=auth_router)

    logger.info("Application run")
    yield
    logger.info("Application shut down")
