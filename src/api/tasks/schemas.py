from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    user_id: int
    completed: bool

    class ConfigDict:
        from_attributes = True


class AddTaskSchema(BaseModel):
    title: str
    description: str | None = None

    class ConfigDict:
        from_attributes = True


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str

    class ConfigDict:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str

    class ConfigDict:
        from_attributes = True
