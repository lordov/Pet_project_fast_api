from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.api.users.models import User
from src.api.users.schemas import UserSchema, UserOut, UserCreate


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def read_users():
    return {"message": "Hello World"}


@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)

    user = result.scalars().first()

    return user


@router.post("/", response_model=UserOut)
async def create_user(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        stmt = insert(User).values(new_user.model_dump())
        await session.execute(stmt)
        await session.commit()
        return new_user

    except Exception as e:
        return {
            "message": "User not created",
            "error": str(e)
        }
