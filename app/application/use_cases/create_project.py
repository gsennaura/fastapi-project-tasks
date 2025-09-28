"""Create project use case."""

from typing import Optional
from datetime import datetime

from ...domain.entities import Project
from ...domain.interfaces import ProjectRepositoryInterface
from ...domain.value_objects import ProjectId
from ..dtos import CreateProjectDTO, ProjectResponseDTO


class CreateProjectUseCase:
    """Use case for creating a new project."""
    
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self._project_repository = project_repository
    
    async def execute(self, dto: CreateProjectDTO) -> ProjectResponseDTO:
        """Execute the create project use case."""
        # Generate new project ID
        project_id = ProjectId.generate()
        
        # Create domain entity
        project = Project(
            id=project_id,
            name=dto.name,
            description=dto.description
        )
        
        # Persist through repository
        created_project = await self._project_repository.create(project)
        
        # Return response DTO
        return ProjectResponseDTO(
            id=str(created_project.id),
            name=created_project.name,
            description=created_project.description,
            created_at=created_project.created_at
        )
