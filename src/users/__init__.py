from fastapi import APIRouter

from .v1.routers import router as v1


users_router = APIRouter(prefix="/users", tags=["users"])

users_router.include_router(v1)
