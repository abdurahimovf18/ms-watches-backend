from fastapi import APIRouter
from .v1.routers import router as v1_router


countries_router = APIRouter(prefix="/countries", tags=["countries"])

countries_router.include_router(v1_router)
