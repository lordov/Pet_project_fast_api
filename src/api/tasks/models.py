from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from src.api.tasks.schemas import TaskSchema
from src.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    completed = Column(Boolean, default=False)

    owner = relationship("User", back_populates="tasks")

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            author_id=self.owner_id,
            completed=self.completed
        )
