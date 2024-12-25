from fastapi import APIRouter
from .schemas import WatchCreateSchema, WatchCreateResponseSchema


router = APIRouter(prefix="/V1", tags=["V1"])


@router.post("/add_watch/")
async def add_watch(watch: WatchCreateSchema) -> WatchCreateResponseSchema:

    print(watch)

    return WatchCreateResponseSchema(ok=True, detail="Watch was created")
