from fastapi import APIRouter

from .v1.routers import router as v1


brands_router = APIRouter(prefix="/brands", tags=["Brands"])

brands_router.include_router(v1)
