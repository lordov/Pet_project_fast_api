from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tasks.schemas import TaskSchema, AddTaskSchema
from src.api.users.schemas import Role, UserSchema

from src.core.security.auth import check_role, get_current_active_user
from src.db.base import get_async_session
from src.db.db import add_task, get_all_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/get_tasks")
@check_role(role=[Role.USER, Role.ADMIN])
async def get_tasks(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_async_session)
):  
    # подумать как возвращать через response_model
    all_tasks = await get_all_tasks(session, current_user.id)
    return all_tasks


@router.post("/add_task", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
@check_role(role=[Role.USER, Role.ADMIN])
async def add_task_to_db(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task: AddTaskSchema,
    session: AsyncSession = Depends(get_async_session),
):
    user_id = current_user.id
    try:
        added_task = await add_task(session, task, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return added_task
