"""Task API routes."""

from typing import List
from fastapi import APIRouter, Depends, status

from ....dependencies import get_task_controller
from ..controllers import TaskController
from ..schemas import (
    CreateTaskRequest, 
    UpdateTaskRequest, 
    TaskResponse, 
    MessageResponse
)


router = APIRouter(tags=["tasks"])


@router.post(
    "/projects/{project_id}/tasks/",
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for a specific project"
)
async def create_task(
    project_id: str,
    request: CreateTaskRequest,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Create a new task for a project."""
    return await controller.create_task(project_id, request)


@router.get(
    "/projects/{project_id}/tasks/",
    response_model=List[TaskResponse],
    summary="Get project tasks",
    description="Get all tasks for a project sorted by priority (descending)"
)
async def get_project_tasks(
    project_id: str,
    page: int = 1,
    page_size: int = 20,
    controller: TaskController = Depends(get_task_controller)
) -> List[TaskResponse]:
    """Get all tasks for a project sorted by priority."""
    return await controller.list_project_tasks(project_id, page, page_size)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID", 
    description="Retrieve a specific task by its ID"
)
async def get_task(
    task_id: str,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Get task by ID."""
    return await controller.get_task(task_id)


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update task properties like title, priority, completion status, or due date"
)
async def update_task(
    task_id: str,
    request: UpdateTaskRequest,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Update task."""
    return await controller.update_task(task_id, request)


@router.delete(
    "/tasks/{task_id}",
    response_model=MessageResponse,
    summary="Delete task",
    description="Delete a specific task"
)
async def delete_task(
    task_id: str,
    controller: TaskController = Depends(get_task_controller)
) -> MessageResponse:
    """Delete task."""
    return await controller.delete_task(task_id)
