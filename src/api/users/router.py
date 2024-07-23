from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.exceptions import UserNotFoundException
from src.db.base import get_async_session
from src.db.db import get_all_user
from src.core.security.auth import check_role, get_current_active_user, oauth2_scheme
from src.api.users.models import User
from src.api.users.schemas import Role, UserOut, UserSchema
from src.exceptions.schemas import ErrorResponseModel


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


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Get user by id",
    description="The ednpoint returns user by id",
    responses={
            status.HTTP_200_OK: {"model": UserOut},
            status.HTTP_404_NOT_FOUND: {"model": ErrorResponseModel},
    },
)
@check_role(role=[Role.USER, Role.ADMIN])
async def read_user(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    user = result.scalars().first()

    if not user:
        raise UserNotFoundException(msg=[f"User with id {user_id} not found"])

    return user
