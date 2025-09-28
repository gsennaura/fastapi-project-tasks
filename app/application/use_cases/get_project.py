"""Get project use case."""

from ...domain.entities import Project
from ...domain.interfaces import ProjectRepositoryInterface
from ...domain.value_objects import ProjectId
from ...domain.exceptions import ProjectNotFoundError
from ..dtos import ProjectResponseDTO


class GetProjectUseCase:
    """Use case for retrieving a project by ID."""
    
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self._project_repository = project_repository
    
    async def execute(self, project_id: str) -> ProjectResponseDTO:
        """Execute the get project use case."""
        # Create value object
        project_id_vo = ProjectId(project_id)
        
        # Get project from repository
        project = await self._project_repository.get_by_id(project_id_vo)
        
        if not project:
            raise ProjectNotFoundError(project_id)
        
        # Return response DTO
        return ProjectResponseDTO(
            id=str(project.id),
            name=project.name,
            description=project.description,
            created_at=project.created_at
        )
