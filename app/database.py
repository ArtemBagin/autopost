from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import as_declarative, declared_attr

from config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@" \
               f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_scoped_session(async_session, scopefunc=current_task)
    try:
        yield session
    finally:
        await session.remove()


@as_declarative()
class Base:
    id = Column(Integer, autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
