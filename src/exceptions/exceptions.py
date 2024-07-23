from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(self, msg: list[str]):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.msg = msg


class UserAlreadyExists(HTTPException):
    def __init__(self, msg: list[str]):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="This user already exist")
        self.msg = msg
