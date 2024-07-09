from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    user_id: int
    completed: bool

    class Config:
        from_attributes = True


class AddTaskSchema(BaseModel):
    title: str
    description: str | None = None

    class Config:
        from_attributes = True
    