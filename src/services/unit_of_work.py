from abc import ABC, abstractmethod
from typing import Type

from db.base import async_session_maker



# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    # users: Type[UsersRepository]
    # tasks: Type[TasksRepository]
    # task_history: Type[TaskHistoryRepository]
    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...
