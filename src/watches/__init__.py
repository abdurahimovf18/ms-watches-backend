from fastapi import APIRouter

from .v1.routers import router as v1


watches_router = APIRouter(prefix="/watches", tags=["watches"])

watches_router.include_router(v1)
