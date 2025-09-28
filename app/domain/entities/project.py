"""Project entity."""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from ..value_objects import ProjectId
from ..exceptions import ProjectValidationError

if TYPE_CHECKING:
    from .task import Task


class Project:
    """Domain entity representing a project."""
    
    def __init__(
        self, 
        id: ProjectId,
        name: str,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self._validate_name(name)
        
        self._id = id
        self._name = name
        self._description = description
        self._created_at = created_at or datetime.utcnow()
        self._tasks: List["Task"] = []
    
    @staticmethod
    def _validate_name(name: str) -> None:
        """Validates the project name."""
        if not name or not name.strip():
            raise ProjectValidationError("Project name cannot be empty")
        if len(name.strip()) > 255:
            raise ProjectValidationError("Project name cannot exceed 255 characters")
    
    @property
    def id(self) -> ProjectId:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def tasks(self) -> List["Task"]:
        """Returns a copy of the tasks list to preserve encapsulation."""
        return self._tasks.copy()
    
    def update_name(self, name: str) -> None:
        """Updates the project name."""
        self._validate_name(name)
        self._name = name.strip()
    
    def update_description(self, description: Optional[str]) -> None:
        """Updates the project description."""
        self._description = description.strip() if description else None
    
    def add_task(self, task: "Task") -> None:
        """Adds a task to the project."""
        if task not in self._tasks:
            self._tasks.append(task)
    
    def remove_task(self, task: "Task") -> None:
        """Removes a task from the project."""
        if task in self._tasks:
            self._tasks.remove(task)
    
    def get_tasks_sorted_by_priority(self) -> List["Task"]:
        """Returns tasks sorted by priority (descending)."""
        return sorted(self._tasks, key=lambda t: t.priority.value, reverse=True)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Project):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
