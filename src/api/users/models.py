from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.api.tasks.models import Task
from src.db.base import Base
from src.api.users.schemas import UserOut

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")

    def to_read_model(self) -> UserOut:
        return UserOut(
            id=self.id,
            email=self.email,
            full_name=self.full_name,
        )