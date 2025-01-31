from fastapi import status, HTTPException
from loguru import logger

from . import cache, db
from ..schemas import router as rs

from src.utils import compile_all, compile_one


async def get_social_links(params: rs.SlReParamSchema) -> list[rs.SlReRespSchema]:
    try:
        db_resp = await cache.get_social_links(params=params)
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    return compile_all(db_resp, rs.SlReRespSchema)
