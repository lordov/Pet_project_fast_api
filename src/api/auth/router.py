from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from src.db.base import get_async_session
from src.db.db import authenticate_user, regisrty_user

from src.api.auth.models import Token
from src.api.dependencies.auth import create_access_token, get_current_active_user
from src.api.users.schemas import UserCreate, UserOut, UserSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],

)

# Присвоение токена при входе в систему


@router.post("/sign_up", response_model=UserOut)
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


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/admin_resource", response_model=UserSchema)
async def admin_permission(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="Acces denied")

    return current_user
