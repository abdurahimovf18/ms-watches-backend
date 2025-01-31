from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, delete, select, and_, or_
from sqlalchemy.dialects.postgresql import dialect

from src.core.database.utils import db_services


from ...models import BrandsModel, BrandImagesModel, CountriesModel, CountryImagesModel
from ..schemas import brands, countries, brand_images, router as rs
from src.countries import constants as country_consts
from ... import constants as consts


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
    async def get_top_brands(cls, params: rs.BrTpParamSchema, session: AsyncSession) -> tuple[dict]:
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
                *cls.country_images_model.cols_from_pyd(countries.BrTpRespSchema),
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

    @db_services.service()
    async def get_brand_placeholders(cls, params: rs.BrPhParamSchema, session: AsyncSession) -> tuple[dict]:
        """
        select * 
        from brands b 
        inner join brand_images bi
        on b.id = bi.brand_id and bi.brand_image_type = 'PLACEHOLDER'
        """
        query = (
            select(
                *cls.brands_model.cols_from_pyd(brands.BrPhRespSchema),
                *cls.brand_img_model.cols_from_pyd(brand_images.BrPhRespSchema)
            )
            .join(
                cls.brand_img_model,
                and_(
                    cls.brands_model.id == cls.brand_img_model.brand_id,
                    cls.brand_img_model.brand_image_type == consts.BrandImageType.PLACEHOLDER
                    
                )
            )
            .limit(params.limit)
        )

        resp = await session.execute(query)
        return cls.rows_to_dict(resp.mappings().all())
