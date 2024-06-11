from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False

    class Config:
        from_attributes = True


class UserInDB(UserSchema):
    hashed_password: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str | None = None
