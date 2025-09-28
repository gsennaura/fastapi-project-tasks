"""Project repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import Project
from ..value_objects import ProjectId


class ProjectRepositoryInterface(ABC):
    """Interface for project repository."""
    
    @abstractmethod
    async def create(self, project: Project) -> Project:
        """Creates a new project."""
        pass
    
    @abstractmethod
    async def get_by_id(self, project_id: ProjectId) -> Optional[Project]:
        """Gets project by ID."""
        pass
    
    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Updates an existing project."""
        pass
    
    @abstractmethod
    async def delete(self, project_id: ProjectId) -> None:
        """Removes a project."""
        pass
    
    @abstractmethod
    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Project]:
        """Lists all projects with optional pagination."""
        pass
    
    @abstractmethod
    async def exists(self, project_id: ProjectId) -> bool:
        """Checks if a project exists."""
        pass
