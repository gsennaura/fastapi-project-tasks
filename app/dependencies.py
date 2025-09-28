"""Dependency injection configuration - following Clean Architecture."""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Infrastructure imports
from .infrastructure.database import get_db_session
from .infrastructure.repositories import ProjectRepository, TaskRepository

# Domain imports (interfaces)
from .domain.interfaces import ProjectRepositoryInterface, TaskRepositoryInterface

# Application imports  
from .application.use_cases import (
    CreateProjectUseCase,
    GetProjectUseCase,
    UpdateProjectUseCase, 
    DeleteProjectUseCase,
    ListProjectsUseCase,
    CreateTaskUseCase
)

# Interface imports
from .interfaces.api.controllers import ProjectController, TaskController


# Infrastructure Layer Dependencies

async def get_database() -> AsyncSession:
    """Get database session dependency."""
    async for session in get_db_session():
        yield session


def get_project_repository(
    db: AsyncSession = Depends(get_database)
) -> ProjectRepositoryInterface:
    """Get project repository dependency."""
    return ProjectRepository(db)


def get_task_repository(
    db: AsyncSession = Depends(get_database)
) -> TaskRepositoryInterface:
    """Get task repository dependency."""
    return TaskRepository(db)


# Application Layer Dependencies

def get_create_project_use_case(
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> CreateProjectUseCase:
    """Get create project use case dependency."""
    return CreateProjectUseCase(project_repo)


def get_get_project_use_case(
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> GetProjectUseCase:
    """Get get project use case dependency."""
    return GetProjectUseCase(project_repo)


def get_update_project_use_case(
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> UpdateProjectUseCase:
    """Get update project use case dependency."""
    return UpdateProjectUseCase(project_repo)


def get_delete_project_use_case(
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> DeleteProjectUseCase:
    """Get delete project use case dependency."""
    return DeleteProjectUseCase(project_repo)


def get_list_projects_use_case(
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> ListProjectsUseCase:
    """Get list projects use case dependency."""
    return ListProjectsUseCase(project_repo)


def get_create_task_use_case(
    task_repo: TaskRepositoryInterface = Depends(get_task_repository),
    project_repo: ProjectRepositoryInterface = Depends(get_project_repository)
) -> CreateTaskUseCase:
    """Get create task use case dependency."""
    return CreateTaskUseCase(task_repo, project_repo)


# Interface Layer Dependencies

def get_project_controller(
    create_project_use_case: CreateProjectUseCase = Depends(get_create_project_use_case),
    get_project_use_case: GetProjectUseCase = Depends(get_get_project_use_case),
    update_project_use_case: UpdateProjectUseCase = Depends(get_update_project_use_case),
    delete_project_use_case: DeleteProjectUseCase = Depends(get_delete_project_use_case),
    list_projects_use_case: ListProjectsUseCase = Depends(get_list_projects_use_case)
) -> ProjectController:
    """Get project controller dependency."""
    return ProjectController(
        create_project_use_case,
        get_project_use_case,
        update_project_use_case,
        delete_project_use_case,
        list_projects_use_case
    )


def get_task_controller(
    create_task_use_case: CreateTaskUseCase = Depends(get_create_task_use_case)
) -> TaskController:
    """Get task controller dependency."""
    return TaskController(create_task_use_case)
