from fastapi import APIRouter

from .v1.routers import router as v1_router


collections_router = APIRouter(prefix="/collections", tags="collections")

collections_router.include_router(v1_router)
