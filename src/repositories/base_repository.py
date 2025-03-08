from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    IntegrityError, NoResultFound,
    MultipleResultsFound, DBAPIError
)

from db.base import Base
from db.models.users import User
from core.exceptions.exceptions import (
    AlreadyExistError, DBError,
    NoRowsFoundError, MultipleRowsFoundError,
)


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
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise AlreadyExistError(
                f'For model {self.model.__name__} already exists'
            )
        return result.scalar_one()

    async def edit_one(self, id: int, data: dict, user_id: Optional[int] = None) -> User:
        if not data:
            raise DBError(
                f'Passed empty dict for update method in model {self.model.__name__}'
            )
        stmt = update(self.model).values(
            **data).where(self.model.id == id).returning(self.model)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id ==
                              user_id).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except NoResultFound:
            raise NoRowsFoundError(
                f'For model {self.model.__name__} not found with id: {id}')
        return result.scalar_one()

    async def get_all(self, user_id: Optional[int] = None):
        query = select(self.model)
        if user_id is not None:
            query = select(self.model).where(self.model.user_id == user_id)
        try:
            result = await self.session.execute(query)
        except NoResultFound:
            raise NoRowsFoundError(
                f'For model {self.model.__name__} not found')
        except DBAPIError as e:
            raise DBError(str(e))

        return result.scalars().all()

    async def delete_one(self, id: int, user_id: Optional[int] = None) -> bool:
        stmt = delete(self.model).where(
            self.model.id == id).returning(self.model)
        if user_id is not None:
            stmt = stmt.where(self.model.user_id ==
                              user_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_one(self, id: int, user_id: Optional[int] = None):
        query = select(self.model).where(self.model.id == id)
        if user_id is not None:
            query = query.where(self.model.user_id == user_id)
        row = await self.session.execute(query)
        try:
            result = row.scalar_one()
        except NoResultFound:
            raise NoRowsFoundError(
                detail=f'For model {self.model.__name__} with id: {id} not found',
                errors=[
                    f'The {self.model.__name__} with the given id does not exist in the database.']
            )
        except MultipleResultsFound:
            raise MultipleRowsFoundError(
                detail=f'For model {self.model.__name__} with id: {id}',
                errors=[
                    f'Multiple {self.model.__name__} records found with the same id. Please check the data integrity.']
            )
        return result
