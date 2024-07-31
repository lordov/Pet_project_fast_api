from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: Role | None = 'guest'
    fullname: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserInDB(UserSchema):
    hashed_password: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    password: str = Field(min_length=8, max_length=64)
    fullname: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    fullname: str | None = None


class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    result: UserOut | None = None
    error: str | None = None
