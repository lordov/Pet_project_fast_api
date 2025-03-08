from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    user_id: int
    completed: bool


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None = None
    completed: bool


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
