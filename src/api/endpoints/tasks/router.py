from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.tasks import (
    TaskSchema, CreateTask,
    TaskResponseSchema, MessageResponse
)
from api.schemas.users import Role, UserSchema

from core.security.auth import check_role, get_current_active_user
from db.base import get_async_session
from db.db import (
    get_one_task_db, update_task_db, delete_task_db
)
from services.tasks_service import TaskService
from utils.unit_of_work import IUnitOfWork, UnitOfWork

router_task = APIRouter(
    tags=["Tasks"],
)


async def get_todo_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)


@router_task.get("/tasks", response_model=list[TaskResponseSchema])
@check_role(role=[Role.USER, Role.ADMIN])
async def get_tasks(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_service: TaskService = Depends(get_todo_service),
):
    # подумать как возвращать через response_model
    return await task_service.get_all_tasks(user_id=current_user.id)


@router_task.get("/tasks/{task_id}", response_model=TaskSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def get_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task_service: TaskService = Depends(get_todo_service),
):
    return await task_service.get_one_task(task_id, current_user.id)


@router_task.put("/tasks/{task_id}", response_model=TaskResponseSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def update_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task: CreateTask,
    task_service: TaskService = Depends(get_todo_service),
):
    return await task_service.update_task(task_id, task, current_user.id)


@router_task.post(
    "/tasks",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
@check_role(role=[Role.USER, Role.ADMIN])
async def create_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task: CreateTask,
    task_service: TaskService = Depends(get_todo_service),
):
    user_id = current_user.id
    return await task_service.add_task(task, user_id)


@router_task.delete(
    "/tasks/{task_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
@check_role(role=[Role.USER, Role.ADMIN])
async def delete_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task_service: TaskService = Depends(get_todo_service),
):
    return await task_service.delete_task(task_id, current_user.id)
