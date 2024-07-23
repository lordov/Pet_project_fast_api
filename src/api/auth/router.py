from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from src.exceptions.exceptions import UserAlreadyExists
from src.exceptions.schemas import ErrorResponseModel
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from src.db.base import get_async_session
from src.db.db import authenticate_user, regisrty_user

from src.api.auth.models import Token
from src.core.security.auth import (
    create_access_token, get_current_active_user,
    check_role
)
from src.api.users.schemas import (
    UserCreate, UserOut,
    UserSchema, Role
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],

)

# Присвоение токена при входе в систему


@router.post(
    "/sign_up",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary='Sign up',
    description='The endpoint creates new user',
    responses={
        status.HTTP_201_CREATED: {"model": UserOut},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponseModel},
    }
)
async def create_user(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserOut:
    try:
        user_saved = await regisrty_user(new_user, session)
        return user_saved
    except ResponseValidationError:
        raise ResponseValidationError
    
    except UserAlreadyExists as uae:
        raise uae
    except Exception as e:
        return {
            "message": "User not created",
            "error": str(e)
        }


@router.post("/token")
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
@check_role(role=[Role.ADMIN])
async def admin_permission(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user
