"""Project controller - Interface Adapter layer."""

from typing import List
from fastapi import HTTPException, status, Query

from ....application.use_cases import (
    CreateProjectUseCase,
    GetProjectUseCase, 
    UpdateProjectUseCase,
    DeleteProjectUseCase,
    ListProjectsUseCase
)
from ....application.dtos import CreateProjectDTO, UpdateProjectDTO, PaginationDTO
from ....domain.exceptions import ProjectNotFoundError, DomainException
from ..schemas import CreateProjectRequest, UpdateProjectRequest, ProjectResponse, MessageResponse


class ProjectController:
    """Controller for project endpoints - Interface Adapter."""
    
    def __init__(
        self,
        create_project_use_case: CreateProjectUseCase,
        get_project_use_case: GetProjectUseCase,
        update_project_use_case: UpdateProjectUseCase,
        delete_project_use_case: DeleteProjectUseCase,
        list_projects_use_case: ListProjectsUseCase
    ):
        self._create_project_use_case = create_project_use_case
        self._get_project_use_case = get_project_use_case
        self._update_project_use_case = update_project_use_case
        self._delete_project_use_case = delete_project_use_case
        self._list_projects_use_case = list_projects_use_case
    
    async def create_project(self, request: CreateProjectRequest) -> ProjectResponse:
        """Create a new project."""
        try:
            dto = CreateProjectDTO(
                name=request.name,
                description=request.description
            )
            
            project_dto = await self._create_project_use_case.execute(dto)
            
            return ProjectResponse(
                id=project_dto.id,
                name=project_dto.name,
                description=project_dto.description,
                created_at=project_dto.created_at
            )
            
        except DomainException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def get_project(self, project_id: str) -> ProjectResponse:
        """Get project by ID."""
        try:
            project_dto = await self._get_project_use_case.execute(project_id)
            
            return ProjectResponse(
                id=project_dto.id,
                name=project_dto.name,
                description=project_dto.description,
                created_at=project_dto.created_at
            )
            
        except ProjectNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id '{project_id}' not found"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def update_project(
        self, 
        project_id: str, 
        request: UpdateProjectRequest
    ) -> ProjectResponse:
        """Update a project."""
        try:
            dto = UpdateProjectDTO(
                name=request.name,
                description=request.description
            )
            
            project_dto = await self._update_project_use_case.execute(project_id, dto)
            
            return ProjectResponse(
                id=project_dto.id,
                name=project_dto.name,
                description=project_dto.description,
                created_at=project_dto.created_at
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
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def delete_project(self, project_id: str) -> MessageResponse:
        """Delete a project."""
        try:
            await self._delete_project_use_case.execute(project_id)
            return MessageResponse(message="Project deleted successfully")
            
        except ProjectNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id '{project_id}' not found"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    async def list_projects(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Page size")
    ) -> List[ProjectResponse]:
        """List all projects with pagination."""
        try:
            pagination = PaginationDTO(page=page, page_size=page_size)
            project_dtos = await self._list_projects_use_case.execute(pagination)
            
            return [
                ProjectResponse(
                    id=dto.id,
                    name=dto.name,
                    description=dto.description,
                    created_at=dto.created_at
                )
                for dto in project_dtos
            ]
            
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
