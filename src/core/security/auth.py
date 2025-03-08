import jwt

from typing import Annotated
from datetime import datetime, timezone, timedelta
from functools import wraps

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.users import UserSchema, Role
from api.schemas.token import TokenData
from db.db import get_user
from db.base import get_async_session
from core.config.jwt import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", scheme_name="JWT")


# Создаем токен

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверяем текущего юзера


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def check_role(role: list[Role]):
    def decorator(func):
        @wraps(func)
        async def wrapper(current_user: Annotated[UserSchema, Depends(get_current_active_user)], *args, **kwargs):
            if current_user.role not in role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acces denied",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return await func(current_user, *args, **kwargs)
        return wrapper
    return decorator
