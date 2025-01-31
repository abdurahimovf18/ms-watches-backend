from fastapi import APIRouter
from .v1.routers import router as v1_router


social_links_router = APIRouter(prefix="/social-links", tags=["social"])

social_links_router.include_router(v1_router)
