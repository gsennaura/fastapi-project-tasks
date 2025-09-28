"""Domain repository interfaces - follow the Dependency Rule."""

from .project_repository import ProjectRepositoryInterface
from .task_repository import TaskRepositoryInterface

__all__ = ["ProjectRepositoryInterface", "TaskRepositoryInterface"]
