from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from config import database_settings


engine = create_async_engine(
    url=database_settings.url,
    echo=database_settings.echo
)
async_session_factory = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    metadata = MetaData()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
