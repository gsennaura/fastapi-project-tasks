"""Project-related exceptions."""

from .base import DomainException


class ProjectNotFoundError(DomainException):
    """Raised when a project is not found."""
    
    def __init__(self, project_id: str):
        message = f"Project with id '{project_id}' not found"
        super().__init__(message, "PROJECT_NOT_FOUND")
        self.project_id = project_id


class ProjectAlreadyExistsError(DomainException):
    """Raised when attempting to create a project that already exists."""
    
    def __init__(self, project_id: str):
        message = f"Project with id '{project_id}' already exists"
        super().__init__(message, "PROJECT_ALREADY_EXISTS")
        self.project_id = project_id


class ProjectValidationError(DomainException):
    """Raised when project data validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, "PROJECT_VALIDATION_ERROR")
