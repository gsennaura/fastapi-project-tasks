"""List projects use case."""

from typing import List, Optional

from ...domain.interfaces import ProjectRepositoryInterface
from ..dtos import PaginationDTO, ProjectResponseDTO


class ListProjectsUseCase:
    """Use case for listing projects with pagination."""
    
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self._project_repository = project_repository
    
    async def execute(self, pagination: Optional[PaginationDTO] = None) -> List[ProjectResponseDTO]:
        """Execute the list projects use case."""
        # Get projects from repository
        if pagination:
            projects = await self._project_repository.list_all(
                limit=pagination.limit,
                offset=pagination.offset
            )
        else:
            projects = await self._project_repository.list_all()
        
        # Convert to response DTOs
        return [
            ProjectResponseDTO(
                id=str(project.id),
                name=project.name,
                description=project.description,
                created_at=project.created_at
            )
            for project in projects
        ]
