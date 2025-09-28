"""Task repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import Task
from ..value_objects import TaskId, ProjectId


class TaskRepositoryInterface(ABC):
    """Interface for task repository."""
    
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """Creates a new task."""
        pass
    
    @abstractmethod
    async def get_by_id(self, task_id: TaskId) -> Optional[Task]:
        """Gets task by ID."""
        pass
    
    @abstractmethod
    async def update(self, task: Task) -> Task:
        """Updates an existing task."""
        pass
    
    @abstractmethod
    async def delete(self, task_id: TaskId) -> None:
        """Removes a task."""
        pass
    
    @abstractmethod
    async def get_by_project_id(
        self, 
        project_id: ProjectId, 
        limit: Optional[int] = None, 
        offset: int = 0
    ) -> List[Task]:
        """Lists tasks from a project ordered by priority (descending)."""
        pass
    
    @abstractmethod
    async def exists(self, task_id: TaskId) -> bool:
        """Checks if a task exists."""
        pass
