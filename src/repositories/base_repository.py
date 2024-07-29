from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from db.base import Base


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

    async def add_one(self, data: dict, user_id: Optional[int] = None) -> int:
        data['user_id'] = user_id
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict, user_id: Optional[int] = None) -> int:
        stmt = update(self.model).values(**data).filter_by(self.model.id == id)
        if user_id is not None:
            stmt = stmt.filter_by(self.model.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, user_id: Optional[int] = None):
        query = select(self.model)
        if user_id is not None:
            query = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_one(self, id: int, user_id: Optional[int] = None) -> bool:
        query = select(self.model).where(self.model.id == id)
        if user_id is not None:
            query = query.where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()

        if not instance:
            return False

        stmt = delete(self.model).where(self.model.id == id)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id == user_id)
        await self.session.execute(stmt)
        return True

    async def get_one(self, id: int, user_id: Optional[int] = None):
        query = select(self.model).where(self.model.id == id)
        if user_id is not None:
            query = query.where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
