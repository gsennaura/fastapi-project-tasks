"""Task controller."""

from typing import List
from fastapi import HTTPException, status, Query

from ....application.use_cases import CreateTaskUseCase
from ....application.dtos import CreateTaskDTO, UpdateTaskDTO, PaginationDTO
from ....domain.exceptions import TaskNotFoundError, ProjectNotFoundError, DomainException
from ..schemas import CreateTaskRequest, UpdateTaskRequest, TaskResponse, MessageResponse


class TaskController:
    """Controller for task endpoints."""
    
    def __init__(self, create_task_use_case: CreateTaskUseCase):
        self._create_task_use_case = create_task_use_case
    
    async def create_task(
        self, 
        project_id: str, 
        request: CreateTaskRequest
    ) -> TaskResponse:
        """Creates a new task for a project."""
        try:
            dto = CreateTaskDTO(
                title=request.title,
                priority=request.priority,
                due_date=request.due_date
            )
            
            task_dto = await self._create_task_use_case.execute(project_id, dto)
            
            return TaskResponse(
                id=task_dto.id,
                project_id=task_dto.project_id,
                title=task_dto.title,
                priority=task_dto.priority,
                completed=task_dto.completed,
                due_date=task_dto.due_date,
                created_at=task_dto.created_at
            )
            
        except ProjectNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id '{project_id}' not found"
            )
        except DomainException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def get_task(self, task_id: str) -> TaskResponse:
        """Gets a task by ID."""
        try:
            task_dto = await self._task_service.get_task(task_id)
            
            return TaskResponse(
                id=task_dto.id,
                project_id=task_dto.project_id,
                title=task_dto.title,
                priority=task_dto.priority,
                completed=task_dto.completed,
                due_date=task_dto.due_date,
                created_at=task_dto.created_at
            )
            
        except TaskNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id '{task_id}' not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def update_task(self, task_id: str, request: UpdateTaskRequest) -> TaskResponse:
        """Updates an existing task."""
        try:
            dto = UpdateTaskDTO(
                title=request.title,
                priority=request.priority,
                completed=request.completed,
                due_date=request.due_date
            )
            
            task_dto = await self._task_service.update_task(task_id, dto)
            
            return TaskResponse(
                id=task_dto.id,
                project_id=task_dto.project_id,
                title=task_dto.title,
                priority=task_dto.priority,
                completed=task_dto.completed,
                due_date=task_dto.due_date,
                created_at=task_dto.created_at
            )
            
        except TaskNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id '{task_id}' not found"
            )
        except DomainException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def delete_task(self, task_id: str) -> dict:
        """Removes a task."""
        try:
            await self._task_service.delete_task(task_id)
            return MessageResponse(message="Task deleted successfully")
            
        except TaskNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id '{task_id}' not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def list_project_tasks(
        self,
        project_id: str,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100)
    ) -> List[TaskResponse]:
        """Lists all tasks from a project ordered by priority."""
        try:
            pagination = PaginationDTO(page=page, page_size=page_size)
            task_dtos = await self._task_service.list_project_tasks(project_id, pagination)
            
            return [
                TaskResponse(
                    id=dto.id,
                    project_id=dto.project_id,
                    title=dto.title,
                    priority=dto.priority,
                    completed=dto.completed,
                    due_date=dto.due_date,
                    created_at=dto.created_at
                )
                for dto in task_dtos
            ]
            
        except ProjectNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id '{project_id}' not found"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
