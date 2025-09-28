"""Delete project use case."""

from ...domain.interfaces import ProjectRepositoryInterface
from ...domain.value_objects import ProjectId
from ...domain.exceptions import ProjectNotFoundError


class DeleteProjectUseCase:
    """Use case for deleting a project."""
    
    def __init__(self, project_repository: ProjectRepositoryInterface):
        self._project_repository = project_repository
    
    async def execute(self, project_id: str) -> None:
        """Execute the delete project use case."""
        # Create value object
        project_id_vo = ProjectId(project_id)
        
        # Check if project exists
        exists = await self._project_repository.exists(project_id_vo)
        if not exists:
            raise ProjectNotFoundError(project_id)
        
        # Delete through repository
        await self._project_repository.delete(project_id_vo)
