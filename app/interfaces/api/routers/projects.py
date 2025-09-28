"""Project API routes."""

from typing import List
from fastapi import APIRouter, Depends, status

from ....dependencies import get_project_controller
from ..controllers import ProjectController
from ..schemas import (
    CreateProjectRequest, 
    UpdateProjectRequest, 
    ProjectResponse, 
    MessageResponse
)


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/", 
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with name and optional description"
)
async def create_project(
    request: CreateProjectRequest,
    controller: ProjectController = Depends(get_project_controller)
) -> ProjectResponse:
    """Create a new project."""
    return await controller.create_project(request)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Retrieve a specific project by its ID"
)
async def get_project(
    project_id: str,
    controller: ProjectController = Depends(get_project_controller)
) -> ProjectResponse:
    """Get project by ID."""
    return await controller.get_project(project_id)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="Update project name and/or description"
)
async def update_project(
    project_id: str,
    request: UpdateProjectRequest,
    controller: ProjectController = Depends(get_project_controller)
) -> ProjectResponse:
    """Update project."""
    return await controller.update_project(project_id, request)


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Delete project",
    description="Delete a project and all its associated tasks"
)
async def delete_project(
    project_id: str,
    controller: ProjectController = Depends(get_project_controller)
) -> MessageResponse:
    """Delete project."""
    return await controller.delete_project(project_id)


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="List all projects",
    description="Get a paginated list of all projects"
)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    controller: ProjectController = Depends(get_project_controller)
) -> List[ProjectResponse]:
    """List all projects with pagination."""
    return await controller.list_projects(page, page_size)
