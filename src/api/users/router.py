from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.db.db import get_user, get_all_user, regisrty_user
from src.core.security.auth import check_role, get_current_active_user, oauth2_scheme
from src.api.users.models import User
from src.api.users.schemas import Role, UserOut, UserSchema


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
@check_role(role=[Role.USER, Role.ADMIN])
async def read_users(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
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
@check_role(role=[Role.USER, Role.ADMIN])
async def read_user(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    user = result.scalars().first()

    return user
