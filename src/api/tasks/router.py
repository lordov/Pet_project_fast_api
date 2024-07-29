from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.tasks.schemas import (
    TaskSchema, AddTaskSchema,
    TaskResponseSchema, MessageResponse
)
from api.users.schemas import Role, UserSchema

from core.security.auth import check_role, get_current_active_user
from db.base import get_async_session
from db.db import (
    get_one_task_db, update_task_db, delete_task_db
)
from services.tasks_service import TaskService
from utils.unit_of_work import IUnitOfWork, UnitOfWork

router_task = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


async def get_todo_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)


@router_task.get("/get_tasks", response_model=list[TaskResponseSchema])
@check_role(role=[Role.USER, Role.ADMIN])
async def get_tasks(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_service: TaskService = Depends(get_todo_service),
):
    # подумать как возвращать через response_model
    return await task_service.get_all_tasks(user_id=current_user.id)


@router_task.get("/get_task/{task_id}", response_model=TaskSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def get_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task_service: TaskService = Depends(get_todo_service),
):
    return await task_service.get_one_task(task_id, current_user.id)


@router_task.put("/update_task/{task_id}", response_model=TaskResponseSchema)
@check_role(role=[Role.USER, Role.ADMIN])
async def update_task(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task_id: int,
    task: AddTaskSchema,
    task_service: TaskService = Depends(get_todo_service),
):
    return await task_service.update_task(task_id, task, current_user.id)


@router_task.post(
    "/add_task",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED
)
@check_role(role=[Role.USER, Role.ADMIN])
async def add_task_to_db(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
    task: AddTaskSchema,
    task_service: TaskService = Depends(get_todo_service),
):
    user_id = current_user.id
    return await task_service.add_task(task, user_id)


@router_task.delete(
    "/delete_task/{task_id}",
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
