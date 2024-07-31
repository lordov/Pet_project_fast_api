from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from db.base import Base
from db.models.users import User


class AbstractRepository(ABC):

    @abstractmethod
    async def delete_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def edit_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict, user_id: Optional[int] = None) -> User:
        if user_id is not None:
            data['user_id'] = user_id
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit_one(self, id: int, data: dict, user_id: Optional[int] = None) -> User:
        stmt = update(self.model).values(**data).where(self.model.id == id).returning(self.model)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id == user_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self, user_id: Optional[int] = None):
        query = select(self.model)
        if user_id is not None:
            query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_one(self, id: int, user_id: Optional[int] = None) -> bool:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id == user_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_one(self, id: int, user_id: Optional[int] = None):
        query = select(self.model).where(self.model.id == id)
        if user_id is not None:
            query = query.where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
