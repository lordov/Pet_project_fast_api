from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    full_name: str | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str | None = None

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    class Config:
        from_attributes = True
