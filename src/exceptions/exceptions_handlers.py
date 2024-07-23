from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from src.exceptions.exceptions import CustomException


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = error["msg"]
        errors.append({"field": field, "msg": msg,
                      "your_input": error["input"]})
    print(errors)  # тут например логируем
    return JSONResponse(status_code=422, content=errors)
