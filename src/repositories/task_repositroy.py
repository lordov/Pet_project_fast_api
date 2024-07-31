from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.tasks import TaskSchema, TaskCreate, TaskResponse
from db.models.tasks import Task
from repositories.base_repository import SQLAlchemyRepository
from sqlalchemy import delete, insert, select, update


class TaskRepository(SQLAlchemyRepository):
    """
    Class for task repository.
    """
    model = Task
    # def __init__(self, session: AsyncSession):
    #     """
    #     Initialize SQLAlchemyTaskRepository.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #     """
    #     self.session = session

    # async def get_all_tasks_db(
    #         self, session: AsyncSession, user_id: int
    # ) -> List[TaskResponseSchema]:
    #     """
    #     Get all tasks for user.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #         user_id: User ID.

    #     Returns:
    #         List of TaskResponseSchema.
    #     """
    #     query = select(Task).where(Task.user_id == user_id)
    #     result = await session.execute(query)
    #     result_model = result.scalars().all()
    #     return result_model

    # async def get_one_task_db(
    #         self, session: AsyncSession, user_id: int, task_id: int
    # ) -> TaskResponseSchema:
    #     """
    #     Get one task for user.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #         user_id: User ID.
    #         task_id: Task ID.

    #     Returns:
    #         TaskResponseSchema or False if not found.
    #     """
    #     query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    #     result = await session.execute(query)
    #     try:
    #         db_dict = result.scalars().all()[0].to_read_model()
    #     except IndexError:
    #         return False
    #     return db_dict

    # async def update_task_db(
    #         self, session: AsyncSession, task: AddTaskSchema, user_id: int, task_id: int
    # ) -> TaskResponseSchema:
    #     """
    #     Update task for user.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #         task: AddTaskSchema.
    #         user_id: User ID.
    #         task_id: Task ID.

    #     Returns:
    #         TaskResponseSchema.

    #     Raises:
    #         HTTPException: If task not found.
    #     """
    #     stmt = (
    #         update(Task)
    #         .where(Task.id == task_id, Task.user_id == user_id)
    #         .values(**task.model_dump())
    #         .returning(Task.id, Task.title, Task.description)
    #     )
    #     result = await session.execute(stmt)
    #     await session.commit()

    #     updated_task = result.fetchone()

    #     if not updated_task:
    #         raise HTTPException(status_code=404, detail="Task not found")

    #     return TaskResponseSchema(
    #         id=updated_task.id,
    #         title=updated_task.title,
    #         description=updated_task.description
    #     )

    # async def delete_task_db(
    #         self, session: AsyncSession, user_id: int, task_id: int
    # ) -> bool:
    #     """
    #     Delete task for user.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #         user_id: User ID.
    #         task_id: Task ID.

    #     Returns:
    #         True if task deleted.
    #     """
    #     stmt = (
    #         delete(Task)
    #         .where(Task.id == task_id, Task.user_id == user_id)
    #         .returning(Task.id, Task.title, Task.description)
    #     )
    #     await session.execute(stmt)
    #     await session.commit()

    #     return True

    # async def add_task_db(
    #         self, session: AsyncSession, task: AddTaskSchema, user_id: int
    # ) -> TaskSchema:
    #     """
    #     Add task for user.

    #     Args:
    #         session: SQLAlchemy AsyncSession.
    #         task: AddTaskSchema.
    #         user_id: User ID.

    #     Returns:
    #         TaskSchema.
    #     """
    #     new_task = Task(**task.model_dump(), user_id=user_id)
    #     session.add(new_task)
    #     await session.commit()
    #     return TaskSchema.model_validate(new_task)
