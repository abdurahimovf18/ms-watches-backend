from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlalchemy import select, insert, delete, update

from src.core.database.utils import db_services

from ...models import UsersModel
from ..schemas import users


class UserDbServices(db_services.DbService):
    model = UsersModel

    @db_services.service(auto_commit=True)
    async def save_user(cls, params: users.UsReParamSchema, session: AsyncSession) -> dict:
        stmt = (
            insert(
                cls.model
            ).values(
                **params.model_dump()
            ).returning(
                *cls.model.cols_from_pyd(
                    users.UsReRespSchema
                )
            )
        )

        resp = await session.execute(stmt)
        return cls.row_to_dict(resp.mappings().one())

    @db_services.service()
    async def get_user_by_id(cls, session: AsyncSession, params: users.UsPkParamSchema) -> dict:
        query = (
            select(
                *cls.model.cols_from_pyd(users.UsPkRespSchema)
            ).where(
                cls.model.id == params.user_id
            )
            .limit(1)
        )
        
        db_resp = await session.execute(query) 
        return cls.row_to_dict(db_resp.mappings().one())
        
    @db_services.service()
    async def get_user_by_email(cls, session: AsyncSession, params: users.UsLgParamSchema) -> dict:
        query = (
            select(
                *cls.model.cols_from_pyd(users.UsLgDbRespSchema)
            ).where(
                cls.model.email == params.email
            )
        )
        
        resp = await session.execute(query)
        return cls.row_to_dict(resp.mappings().one())
        