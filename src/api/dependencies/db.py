from typing import Annotated
from fastapi import Depends
from src.api.dependencies.auth import oauth2_scheme


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
): ...
