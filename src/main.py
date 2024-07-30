from fastapi.encoders import jsonable_encoder
import uvicorn

from fastapi import (
    FastAPI, Depends, Request
)

from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates

from api.router import all_routers

from exceptions.exceptions import (
    CustomException, UserNotFoundException,
    UserAlreadyExists
)
from exceptions.exceptions_handlers import (
    custom_exception_handler, validation_exception_handler,
    user_not_found_exception_handler,
    user_already_exists_handler
)
from api.middleware.middleware import additional_processing, logging_middleware


app = FastAPI(
    title="FastAPI project",
)


# Указываем директорию с шаблонами
templates = Jinja2Templates(directory="templates")

app.middleware("http")(logging_middleware)
app.middleware("http")(additional_processing)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError,
                          validation_exception_handler)
app.add_exception_handler(UserNotFoundException,
                          user_not_found_exception_handler)
app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)


for router in all_routers:
    app.include_router(router)


@app.get('/')
async def html_answer(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
