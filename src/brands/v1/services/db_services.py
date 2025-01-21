from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select, and_, or_

from src.core.database.utils import db_services


from ...models import BrandsModel, BrandImagesModel, CountriesModel, CountryImagesModel
from ..schemas import brands, countries
from src.countries import constants as country_consts


class BrandDbServices(db_services.DbService):
    brands_model = BrandsModel
    brand_img_model = BrandImagesModel
    countries_model = CountriesModel
    country_images_model = CountryImagesModel

    # @db_services.service(auto_commit=True)
    # async def create_brand(cls, new_brand: BrandCreateSchema, session: AsyncSession) -> dict:
    #     stmt = insert(cls.model).values(**new_brand.model_dump()).returning(
    #         *cls.model_cols(*BrandCreateResponseSchema.model_fields.keys()))

    #     db_resp = await session.execute(stmt)
    #     resp = db_resp.mappings().one()

    #     return cls.row_to_dict(resp)

    @db_services.service()
    async def get_top_brands(cls, params: brands.BrTpParamSchema, session: AsyncSession) -> tuple[dict]:
        """
        select *
        from brands b
        join country_images
        on b.country_id = c.country_image and c.country_image_type = 'ICON'
        limit 10
        """

        query = (
            select(
                *cls.brands_model.cols_from_pyd(brands.BrTpRespSchema),
                *cls.country_images_model.cols_from_pyd(brands.BrTpRespSchema),
            ).join(
                cls.brands_model,
                and_(
                    cls.brands_model.country_id == cls.country_images_model.country_id,
                    cls.country_images_model.country_image_type == country_consts.CountryImageTypes.ICON.value
                )
            )
            .limit(params.limit)
        )

        resp = await session.execute(query)
        return cls.rows_to_dict(resp.mappings().all())
    