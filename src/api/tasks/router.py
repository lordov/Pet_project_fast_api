from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tasks.schemas import TaskSchema, AddTaskSchema, TaskResponseSchema
from src.api.users.schemas import Role, UserSchema

from src.core.security.auth import check_role, get_current_active_user
from src.db.base import get_async_session
from src.db.db import add_task, get_all_tasks_db, get_task_db, update_task_db

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
    all_tasks = await get_all_tasks_db(session, current_user.id)
    return all_tasks


@router.get("/get_task/{task_id}", response_model=TaskSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def get_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    task = await get_task_db(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/update_task/{task_id}", response_model=TaskResponseSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def update_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task: AddTaskSchema,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        task_db = await update_task_db(session, task, task_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return task_db

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
