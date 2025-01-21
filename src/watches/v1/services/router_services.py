from typing import Generator

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError, NoResultFound
from loguru import logger

from . import db, cache
from ..schemas import watch


async def get_featured_watches(params: watch.WaFeParamSchema) -> list[watch.WaFeRespSchema]:
    try:
        db_resp: tuple[dict] = await cache.get_featured_watches(params=params)
        resp = [watch.WaFeRespSchema(**row) for row in db_resp]
    except NoResultFound as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No featured watch found")
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

    return resp


async def get_top_weekly_watches(params: watch.WaTwParamSchema) -> list[watch.WaTwRespSchema]:
    try:
        db_resp: dict = await cache.get_top_weekly_watches(params=params)
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
    # return watch.WaTwRespSchema(**db_resp)

    return list(map(lambda value: watch.WaTwRespSchema(**value), db_resp))


async def get_new_arrivals(params: watch.WaNaParamSchema) -> list[watch.WaNaRespSchema]:
    try:
        db_resp: Generator[dict, None, None] = await cache.get_new_arrivals(params=params)
        resp = [watch.WaFeRespSchema(**row) for row in db_resp]
    except NoResultFound as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No new arrivals found")
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")

    return resp
