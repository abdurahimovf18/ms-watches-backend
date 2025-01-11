from typing import Generator
from sqlalchemy import select, insert, update, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.utils.db_services import db_services
from ...models import WatchDescriptionsModel, WatchesModel, WatchImagesModel
from ...import constants as consts
from ..schemas import watch, image, description


class WatchDbServices(db_services.DbService):
    watch_model = WatchesModel
    img_model = WatchImagesModel
    desc_model = WatchDescriptionsModel

    @db_services.service()
    async def create_watch(cls, session, **kwargs):
        pass
        
    @db_services.service()
    async def get_featured_watches(cls, session, params: watch.WaFeParamSchema) -> Generator[dict, None, None]:
        query = (
            select(
                *cls.watch_model.cols_from_pyd(watch.WaFeRespSchema),
                *cls.img_model.cols_from_pyd(watch.WaFeRespSchema)
            ).join(
                cls.watch_model,
                and_(
                    cls.img_model.watch_id == cls.watch_model.id, 
                    cls.img_model.image_type == consts.WatchImageType.FEATURED
                )
            ).order_by(cls.watch_model.created_at.desc())
            .limit(params.limit)
        )

        resp = await session.execute(query)
        return (cls.row_to_dict(row) for row in resp.mappings().all())

    @db_services.service()
    async def get_top_weekly_watch(cls, session: AsyncSession, params: watch.WaTwParamSchema) -> dict:
        query = (
            select(
                *cls.watch_model.cols_from_pyd(watch.WaTwRespSchema),
                *cls.img_model.cols_from_pyd(watch.WaTwRespSchema)
            ).join(
                cls.watch_model,
                and_(
                    cls.img_model.watch_id == cls.watch_model.id, 
                    cls.img_model.image_type == consts.WatchImageType.FEATURED
                )
            ).order_by(cls.watch_model.created_at.desc())
            .limit(1)
        )

        resp = await session.execute(query)
        return cls.row_to_dict(resp.mappings().one())

    @db_services.service()
    async def get_new_arrivals(cls, session: AsyncSession, params: watch.WaNaParamSchema) -> Generator[dict, None, None]:
        """
        select w.*, i.*
        from watches w
        join images i
            on w.id = i.watch_id
            and i.image_type = 'FEATURED'
        order by w.created_at
        limit 4;
        """

        query = (
            select(
                *cls.watch_model.cols_from_pyd(watch.WaSaveDbRespSchema),
                *cls.img_model.cols_from_pyd(watch.WaSaveDbRespSchema)
            ).join(
                cls.watch_model,
                and_(
                    cls.img_model.watch_id == cls.watch_model.id, 
                    cls.img_model.image_type == consts.WatchImageType.FEATURED
                )
            ).limit(params.limit)
            .order_by(cls.watch_model.created_at)
        )

        resp = await session.execute(query)
        return (cls.row_to_dict(row) for row in resp.mappings().all())
