from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.core.log

from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application run")
    yield
    logger.info("Application shut down")
