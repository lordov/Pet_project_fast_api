from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.db.db import get_user, get_all_user, regisrty_user
from src.core.security.auth import oauth2_scheme
from src.api.users.models import User
from src.api.users.schemas import UserCreate, UserSchema, UserOut


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def read_users(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_async_session)
):
    result = await get_all_user(session)
    return {"token": token,
            "result": result}


# @router.get("/me")
# async def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
#     return {"current_user": current_user}


@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    user = result.scalars().first()

    return user



