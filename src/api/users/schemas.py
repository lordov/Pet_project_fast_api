from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role | None = 'guest'
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False

    class ConfigDict:
        from_attributes = True


class UserInDB(UserSchema):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=16, max_length=64)
    full_name: str | None = None

    class ConfigDict:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str | None = None


class ResponseModel(BaseModel):
    message: str
    result: UserOut | None = None
    error: str | None = None
