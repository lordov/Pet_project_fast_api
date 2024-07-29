from fastapi import HTTPException
from api.tasks.schemas import TaskSchema, AddTaskSchema, TaskResponseSchema
from utils.unit_of_work import IUnitOfWork
from api.tasks.models import Task


class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_task(self, data: AddTaskSchema, user_id: int) -> TaskSchema:
        async with self.uow:
            try:
                task: Task = await self.uow.task.add_one(data.model_dump(), user_id=user_id)
                task_to_return = TaskSchema.model_validate(task)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            await self.uow.commit()
            return task_to_return

    async def get_all_tasks(self, user_id: int) -> list[TaskResponseSchema]:
        async with self.uow:
            try:
                tasks = await self.uow.task.get_all(user_id=user_id)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
            return [TaskResponseSchema.model_validate(task) for task in tasks]
