from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
    errors: list[str]
