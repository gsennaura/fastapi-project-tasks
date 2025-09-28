"""Task entity."""

from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from ..value_objects import TaskId, ProjectId, Priority

if TYPE_CHECKING:
    from .project import Project


class Task:
    """Domain entity representing a task."""
    
    def __init__(
        self,
        id: TaskId,
        project_id: ProjectId,
        title: str,
        priority: Priority,
        completed: bool = False,
        due_date: Optional[date] = None,
        created_at: Optional[datetime] = None
    ):
        self._validate_title(title)
        
        self._id = id
        self._project_id = project_id
        self._title = title
        self._priority = priority
        self._completed = completed
        self._due_date = due_date
        self._created_at = created_at or datetime.utcnow()
    
    @staticmethod
    def _validate_title(title: str) -> None:
        """Validates the task title."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title.strip()) > 255:
            raise ValueError("Task title cannot exceed 255 characters")
    
    @property
    def id(self) -> TaskId:
        return self._id
    
    @property
    def project_id(self) -> ProjectId:
        return self._project_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def priority(self) -> Priority:
        return self._priority
    
    @property
    def completed(self) -> bool:
        return self._completed
    
    @property
    def due_date(self) -> Optional[date]:
        return self._due_date
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    def update_title(self, title: str) -> None:
        """Updates the task title."""
        self._validate_title(title)
        self._title = title.strip()
    
    def update_priority(self, priority: Priority) -> None:
        """Updates the task priority."""
        self._priority = priority
    
    def mark_as_completed(self) -> None:
        """Marks the task as completed."""
        self._completed = True
    
    def mark_as_incomplete(self) -> None:
        """Marks the task as incomplete."""
        self._completed = False
    
    def update_due_date(self, due_date: Optional[date]) -> None:
        """Updates the due date."""
        if due_date and due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        self._due_date = due_date
    
    def is_overdue(self) -> bool:
        """Checks if the task is overdue."""
        if not self._due_date or self._completed:
            return False
        return self._due_date < date.today()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
