import uvicorn

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Request, status, Depends

from fastapi.exceptions import ResponseValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


from src.api.users.schemas import UserSchema
from src.db.base import get_async_session
from src.db.db import get_user
from src.api.users.models import User
from src.api.router import all_routers
from src.api.dependencies.auth import (
    get_current_active_user, password_hasher, verify_password
)


app = FastAPI(
    title="FastAPI project",
)

# Указываем директорию с шаблонами
templates = Jinja2Templates(directory="templates")

# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
# @app.exception_handler(ResponseValidationError)
# async def validation_exception_handler(request: Request, exc: ResponseValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()}),
#     )

for router in all_routers:
    app.include_router(router)


async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSession
):
    user: User = await get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token")
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
    return {"access_token": user.username, "token_type": "bearer"}


@app.get('/')
async def html_answer(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.post('/calculate')
async def calculate_sum(num1: int, num2: int):
    result = num1 + num2
    return {"result": result}


@app.get("/mine")
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
