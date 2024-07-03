import uvicorn

from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Request, status, Depends

from fastapi.exceptions import ResponseValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


from src.api.users.schemas import UserOut, UserSchema
from src.api.router import all_routers
from src.api.auth.models import Token

from src.api.dependencies.auth import (
    get_current_active_user, create_access_token
)

from src.db.base import get_async_session
from src.db.db import authenticate_user
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


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


@app.get('/')
async def html_answer(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/mine", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
