from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from .schemas import watch
from .services import router_services as services


router = APIRouter(prefix="/v1", tags=["V1"])


# @router.post("/add_watch")
# async def add_watch(watch: WatchCreateSchema) -> WatchCreateResponseSchema:
#     return JSONResponse(content={"ok": True}, status_code=status.HTTP_201_CREATED)


@router.get(
    "/featured",
    summary="Get Featured Watches",
    description="Fetch a list of featured watches based on the provided parameters."
)
async def get_featured_watches(params: watch.WaFeParamSchema = Depends()) -> list[watch.WaFeRespSchema]:
    resp = await services.get_featured_watches(params=params)
    return resp


@router.get(
    "/top-weekly",    
)
async def get_top_weekly_watches(params: watch.WaTwParamSchema = Depends()) -> list[watch.WaTwRespSchema]:
    resp = await services.get_top_weekly_watches(params=params)
    return resp


@router.get(
    "/new-arrivals"
)
async def get_new_arrivals(params: watch.WaNaParamSchema = Depends()) -> list[watch.WaNaRespSchema]:
    resp = await services.get_new_arrivals(params=params)
    return resp
