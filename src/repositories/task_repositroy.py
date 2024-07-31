from db.models.tasks import Task
from repositories.base_repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    """
    Class for task repository.
    """
    model = Task
