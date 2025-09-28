"""Create task use case."""

from ...domain.entities import Task
from ...domain.interfaces import TaskRepositoryInterface, ProjectRepositoryInterface  
from ...domain.value_objects import TaskId, ProjectId, Priority
from ...domain.exceptions import ProjectNotFoundError
from ..dtos import CreateTaskDTO, TaskResponseDTO


class CreateTaskUseCase:
    """Use case for creating a new task."""
    
    def __init__(
        self, 
        task_repository: TaskRepositoryInterface,
        project_repository: ProjectRepositoryInterface
    ):
        self._task_repository = task_repository
        self._project_repository = project_repository
    
    async def execute(self, project_id: str, dto: CreateTaskDTO) -> TaskResponseDTO:
        """Execute the create task use case."""
        # Create value objects
        project_id_vo = ProjectId(project_id)
        task_id = TaskId.generate()
        priority = Priority(dto.priority)
        
        # Verify project exists (business rule)
        project_exists = await self._project_repository.exists(project_id_vo)
        if not project_exists:
            raise ProjectNotFoundError(project_id)
        
        # Create domain entity
        task = Task(
            id=task_id,
            project_id=project_id_vo,
            title=dto.title,
            priority=priority,
            due_date=dto.due_date
        )
        
        # Persist through repository
        created_task = await self._task_repository.create(task)
        
        # Return response DTO
        return TaskResponseDTO(
            id=str(created_task.id),
            project_id=str(created_task.project_id),
            title=created_task.title,
            priority=created_task.priority.value,
            completed=created_task.completed,
            due_date=created_task.due_date,
            created_at=created_task.created_at
        )
