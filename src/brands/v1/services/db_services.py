from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select

from src.core.database.utils import db_services


from ...models import BrandsModel, BrandImagesModel
from ..schemas import BrandCreateSchema, BrandCreateResponseSchema


class BrandDbServices(db_services.DbService):
    model = BrandsModel
    images_model = BrandImagesModel

    @db_services.service(auto_commit=True)
    async def create_brand(cls, new_brand: BrandCreateSchema, session: AsyncSession) -> dict:
        stmt = insert(cls.model).values(**new_brand.model_dump()).returning(
            *cls.model_cols(*BrandCreateResponseSchema.model_fields.keys()))

        db_resp = await session.execute(stmt)
        resp = db_resp.mappings().one()

        return cls.row_to_dict(resp)
