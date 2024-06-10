from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import (
    DB_HOST_PET, DB_NAME_PET,
    DB_PASS_PET, DB_PORT_PET, DB_USER_PET
)

# Не забыть поменять в alembic.ini
DATABASE_URL = f"postgresql+asyncpg://{DB_USER_PET}:{DB_PASS_PET}@{DB_HOST_PET}:{DB_PORT_PET}/{DB_NAME_PET}"
# Для базовых тестов
DATABASE_LITE = "sqlite+aiosqlite:///sqlite.db"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
