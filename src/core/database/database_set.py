from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from .database_settings import DB_ASYNC_URL


engine = create_async_engine(DB_ASYNC_URL)

session_factory: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    autoflush=True,
)

default_metadata = MetaData()
