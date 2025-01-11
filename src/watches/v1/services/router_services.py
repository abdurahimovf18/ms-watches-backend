from typing import Generator

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError, NoResultFound
from loguru import logger

from . import db, cache
from ..schemas import watch


async def get_featured_watches(params: watch.WaFeParamSchema) -> list[watch.WaFeRespSchema]:
    try:
        db_resp: Generator[dict, None, None] = await db.get_featured_watches(params=params)
        resp = [watch.WaFeRespSchema(**row) for row in db_resp]
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    return resp


async def get_top_weekly_watch(params: watch.WaTwParamSchema):
    try:
        db_resp: dict = await db.get_top_weekly_watch(params=params)
    except NoResultFound as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Result not found")
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    return watch.WaTwRespSchema(**db_resp)


async def get_new_arrivals(params: watch.WaNaParamSchema) -> list[watch.WaNaRespSchema]:
    try:
        db_resp: Generator[dict, None, None] = await db.get_new_arrivals(params=params)
        resp = [watch.WaFeRespSchema(**row) for row in db_resp]
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")

    return resp