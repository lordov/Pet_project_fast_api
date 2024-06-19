from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.users.models import User
from src.api.users.schemas import UserCreate
from src.api.dependencies.auth import password_hasher


async def regisrty_user(
        user_in: UserCreate,
        session: AsyncSession
) -> User:
    hashed_password = password_hasher(user_in.password)
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


async def get_user(username, session: AsyncSession):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    try:
        db_dict = result.scalars().all()[0].to_read_model()
    except IndexError:
        return False
    return db_dict


async def get_all_user(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    try:
        db_dict = result.scalars().all()
    except IndexError:
        return False
    return db_dict
