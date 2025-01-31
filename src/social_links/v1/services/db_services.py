from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.utils.db_services import db_services
from ...models import SocialLinksModel

from ..schemas import social_links, router as rs



class SocialLinksDbServices(db_services.DbService):
    social_links_model = SocialLinksModel

    @db_services.service()
    async def get_social_links(cls, session: AsyncSession, params: rs.SlReParamSchema) -> tuple[dict]:
        query = (
            select(
                *cls.social_links_model.cols_from_pyd(social_links.SlReRespSchema)
            )
        )

        if params.limit > -1:
            query = query.limit(params.limit)

        resp = await session.execute(query)
        return cls.rows_to_dict(resp.mappings().all())
