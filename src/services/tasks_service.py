from fastapi import HTTPException
from api.schemas.tasks import MessageResponse, TaskSchema, CreateTask, TaskResponseSchema
from utils.unit_of_work import IUnitOfWork
from db.models.tasks import Task


class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_task(self, data: CreateTask, user_id: int) -> TaskSchema:
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

    async def get_one_task(self, task_id: int, user_id: int) -> TaskSchema:
        async with self.uow:
            task = await self.uow.task.get_one(id=task_id, user_id=user_id)
            if not task:
                raise HTTPException(
                    status_code=404, detail="Task not found")
            return TaskSchema.model_validate(task)

    async def update_task(self, task_id: int, data: CreateTask, user_id: int) -> TaskResponseSchema:
        async with self.uow:
            uppdated_task = await self.uow.task.edit_one(id=task_id, data=data.model_dump(), user_id=user_id)
            await self.uow.commit()
            return TaskResponseSchema.model_validate(uppdated_task)

    async def delete_task(self, task_id: int, user_id: int):
        async with self.uow:
            deleted_task = await self.uow.task.delete_one(id=task_id, user_id=user_id)
            await self.uow.commit()
            return MessageResponse(message=f"Task №{deleted_task.id} deleted successfully")
