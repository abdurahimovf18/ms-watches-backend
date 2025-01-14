from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine

from .database_settings import DB_ASYNC_URL, DB_SYNC_URL


engine = create_async_engine(DB_ASYNC_URL, pool_size=100)

session_factory: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    autoflush=True
)

default_metadata = MetaData()
