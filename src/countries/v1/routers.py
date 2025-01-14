from fastapi import APIRouter

from .services import router_services as services


router = APIRouter(prefix="/V1", tags=["V1"])
