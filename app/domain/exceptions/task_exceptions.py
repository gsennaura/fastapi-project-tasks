"""Task-related exceptions."""

from .base import DomainException


class TaskNotFoundError(DomainException):
    """Raised when a task is not found."""
    
    def __init__(self, task_id: str):
        message = f"Task with id '{task_id}' not found"
        super().__init__(message, "TASK_NOT_FOUND")
        self.task_id = task_id


class TaskAlreadyExistsError(DomainException):
    """Raised when attempting to create a task that already exists."""
    
    def __init__(self, task_id: str):
        message = f"Task with id '{task_id}' already exists"
        super().__init__(message, "TASK_ALREADY_EXISTS")
        self.task_id = task_id
