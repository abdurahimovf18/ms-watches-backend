from fastapi import APIRouter

from .v1.routers import router as v1_router


tags_router = APIRouter(prefix="/tags", tags=["tags"])

tags_router.include_router(v1_router)
