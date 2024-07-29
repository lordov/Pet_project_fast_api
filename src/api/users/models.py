from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from api.tasks.models import Task
from db.base import Base
from api.users.schemas import UserInDB


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    fullname = Column(String, index=True)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")

    def to_read_model(self) -> UserInDB:
        return UserInDB(
            id=self.id,
            email=self.email,
            full_name=self.fullname,
            role=self.role,
            username=self.username,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
        )
