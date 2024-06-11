from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import ResponseValidationError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.db.db import regisrty_user
from src.api.dependencies.auth import oauth2_scheme
from src.api.users.models import User
from src.api.users.schemas import UserCreate, UserSchema, UserOut


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def read_users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# @router.get("/me")
# async def read_users_me(current_user: Annotated[str, Depends(get_current_user)]):
#     return {"current_user": current_user}


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    user = result.scalars().first()

    return user


@router.post("/regisrty", response_model=UserOut)
async def create_user(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserOut:
    try:
        user_saved = await regisrty_user(new_user, session)
        return user_saved
    except ResponseValidationError:
        raise ResponseValidationError
    except Exception as e:
        return {
            "message": "User not created",
            "error": str(e)
        }
