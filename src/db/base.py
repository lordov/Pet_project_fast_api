from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# Не забыть поменять в alembic.ini
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Для базовых тестов
DATABASE_LITE = "sqlite+aiosqlite:///sqlite.db"

engine = create_async_engine(DATABASE_LITE)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
