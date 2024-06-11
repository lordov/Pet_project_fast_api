from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.api.tasks.models import Task
from src.db.base import Base
from src.api.users.schemas import UserInDB


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")

    def to_read_model(self) -> UserInDB:
        return UserInDB(
            id=self.id,
            email=self.email,
            full_name=self.full_name,
            username=self.username,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
        )


fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "supersecretsecret",
        "is_active": True,
    },
    "alice": {
        "id": 2,
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "supersecretsecret2",
        "is_active": False,
    },
}
