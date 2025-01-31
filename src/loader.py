from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

import src.core.log
from .users import users_router
from .watches import watches_router
from .brands import brands_router
from .tags import tags_router
from .countries import countries_router
from .social_links import social_links_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.include_router(router=watches_router)
    app.include_router(router=users_router)
    app.include_router(router=brands_router)
    app.include_router(router=tags_router)
    app.include_router(router=countries_router)
    app.include_router(router=social_links_router)

    logger.info("Application run")     
    yield
    logger.info("Application shut down")
