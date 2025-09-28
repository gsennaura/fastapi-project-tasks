"""Update project use case."""

from ...domain.entities import Project
from ...domain.interfaces import ProjectRepositoryInterface
from ...domain.value_objects import ProjectId
from ...domain.exceptions import ProjectNotFoundError
from ..dtos import UpdateProjectDTO, ProjectResponseDTO


class UpdateProjectUseCase:
    """Use case for updating a project."""
    
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self._project_repository = project_repository
    
    async def execute(self, project_id: str, dto: UpdateProjectDTO) -> ProjectResponseDTO:
        """Execute the update project use case."""
        # Create value object
        project_id_vo = ProjectId(project_id)
        
        # Get existing project
        project = await self._project_repository.get_by_id(project_id_vo)
        
        if not project:
            raise ProjectNotFoundError(project_id)
        
        # Apply updates following domain rules
        if dto.name is not None:
            project.update_name(dto.name)
        
        if dto.description is not None:
            project.update_description(dto.description)
        
        # Persist changes
        updated_project = await self._project_repository.update(project)
        
        # Return response DTO
        return ProjectResponseDTO(
            id=str(updated_project.id),
            name=updated_project.name,
            description=updated_project.description,
            created_at=updated_project.created_at
        )
