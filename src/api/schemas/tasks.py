from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    user_id: int
    completed: bool


class CreateTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None = None


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
