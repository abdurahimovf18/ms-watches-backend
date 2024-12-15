from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from src.core.database.utils import BaseService
from ..models import UsersModel
from ..schemas import UserRegisterSchema
from src.core.database.utils import service_decorator


class UsersService(BaseService):
    model = UsersModel

    @service_decorator(auto_commit=True)
    async def save_user(cls, new_user: UserRegisterSchema, session: AsyncSession) -> bool:
        
        stmt = insert(cls.model).values(**new_user.model_dump())

        try:
            await session.execute(stmt)
        except IntegrityError:
            return False
        
        return True

    @service_decorator()
    async def get_user_by_id(cls, session: AsyncSession, user_id: int) -> dict:
        query = select(cls.model).filter(cls.model.id == user_id).limit(1)

        db_resp = await session.execute(query) 

        if user := db_resp.scalar_one_or_none():
            return cls.model_to_dict(user)
        
        return {}
    
    @service_decorator()
    async def get_user_by_email(cls, session: AsyncSession, email: str) -> dict:

        query = select(cls.model.id, cls.model.password).where(cls.model.email == email).limit(1)
        
        db_resp = await session.execute(query)
        db_resp = db_resp.mappings().one_or_none()

        resp = cls.row_to_dict(db_resp)

        return resp
    