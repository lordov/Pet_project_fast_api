import uvicorn
from fastapi import FastAPI, Request, status

from fastapi.exceptions import ValidationException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.api.router import all_routers

app = FastAPI(
    title="FastAPI project",
)

# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
