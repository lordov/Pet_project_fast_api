from typing import Annotated

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from src.api.users.schemas import UserSchema
from src.api.users.schemas import UserSchema, UserInDB
from src.api.users.models import fake_users_db, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def fake_decode_token(token: str) -> UserSchema:
    return UserSchema(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


def password_hasher(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
