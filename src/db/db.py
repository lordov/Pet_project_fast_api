from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.api.users.models import User
from src.api.users.schemas import UserInDB, UserCreate
from src.api.dependencies.auth import oauth2_scheme


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


async def regisrty_user(
        user_in: UserCreate,
        session: AsyncSession
) -> User:
    hashed_password = fake_password_hasher(user_in.password)
    user_data = user_in.model_dump()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]

    try:
        stmt = insert(User).values(**user_data)
        result = await session.execute(stmt)
        await session.commit()

        # Получение сгенерированного ID
        user_id = result.inserted_primary_key[0]

        # Получение пользователя из базы данных по сгенерированному ID
        user_saved = await session.get(User, user_id)
        return user_saved

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def get_user(id, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return result
