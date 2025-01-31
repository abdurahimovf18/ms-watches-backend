from fastapi import status, HTTPException

from sqlalchemy.exc import IntegrityError
from loguru import logger

from . import db, cache
from ..schemas import brands, countries, router as rs

from src.utils import compile_all, compile_one



async def get_top_brands(params: rs.BrTpParamSchema) -> list[rs.BrTpRespSchema]:
    try:
        db_resp = await cache.get_top_brands(params=params)
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return compile_all(db_resp, rs.BrTpRespSchema)


async def get_brand_placeholders(params: rs.BrPhParamSchema) -> list[rs.BrPhRespSchema]:
    try:
        db_resp = await cache.get_brand_placeholders(params=params)
    except Exception as exc:
        logger.error(str(exc))
    return compile_all(db_resp, rs.BrPhRespSchema)
