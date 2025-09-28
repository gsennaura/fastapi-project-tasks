"""Project repository with SQLAlchemy."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ...domain.entities import Project
from ...domain.interfaces import ProjectRepositoryInterface
from ...domain.value_objects import ProjectId
from ...domain.exceptions import ProjectNotFoundError
from ..database.models import ProjectModel


class ProjectRepository(ProjectRepositoryInterface):
    """Project repository using SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def create(self, project: Project) -> Project:
        """Creates a new project."""
        db_project = ProjectModel(
            id=project.id.value,
            name=project.name,
            description=project.description,
            created_at=project.created_at
        )
        
        self._session.add(db_project)
        await self._session.commit()
        await self._session.refresh(db_project)
        
        return self._model_to_entity(db_project)
    
    async def get_by_id(self, project_id: ProjectId) -> Optional[Project]:
        """Gets project by ID."""
        stmt = (
            select(ProjectModel)
            .options(selectinload(ProjectModel.tasks))
            .where(ProjectModel.id == project_id.value)
        )
        result = await self._session.execute(stmt)
        db_project = result.scalar_one_or_none()
        
        if not db_project:
            return None
        
        return self._model_to_entity(db_project)
    
    async def update(self, project: Project) -> Project:
        """Updates an existing project."""
        stmt = select(ProjectModel).where(ProjectModel.id == project.id.value)
        result = await self._session.execute(stmt)
        db_project = result.scalar_one_or_none()
        
        if not db_project:
            raise ProjectNotFoundError(str(project.id))
        
        db_project.name = project.name
        db_project.description = project.description
        
        await self._session.commit()
        await self._session.refresh(db_project)
        
        return self._model_to_entity(db_project)
    
    async def delete(self, project_id: ProjectId) -> None:
        """Removes a project."""
        stmt = select(ProjectModel).where(ProjectModel.id == project_id.value)
        result = await self._session.execute(stmt)
        db_project = result.scalar_one_or_none()
        
        if not db_project:
            raise ProjectNotFoundError(str(project_id))
        
        await self._session.delete(db_project)
        await self._session.commit()
    
    async def list_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Project]:
        """Lists all projects with optional pagination."""
        stmt = (
            select(ProjectModel)
            .options(selectinload(ProjectModel.tasks))
            .offset(offset)
        )
        
        if limit:
            stmt = stmt.limit(limit)
        
        result = await self._session.execute(stmt)
        db_projects = result.scalars().all()
        
        return [self._model_to_entity(db_project) for db_project in db_projects]
    
    async def exists(self, project_id: ProjectId) -> bool:
        """Checks if a project exists."""
        stmt = select(ProjectModel.id).where(ProjectModel.id == project_id.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def _model_to_entity(self, db_project: ProjectModel) -> Project:
        """Converts SQLAlchemy model to domain entity."""
        from ...domain.entities import Task
        from ...domain.value_objects import TaskId, Priority
        
        project = Project(
            id=ProjectId(db_project.id),
            name=db_project.name,
            description=db_project.description,
            created_at=db_project.created_at
        )
        
        # Add tasks if loaded (check if the relationship was eagerly loaded)
        tasks_loaded = getattr(db_project, '__dict__', {}).get('tasks', None)
        if tasks_loaded is not None:
            for task_model in tasks_loaded:
                task = Task(
                    id=TaskId(task_model.id),
                    project_id=ProjectId(task_model.project_id),
                    title=task_model.title,
                    priority=Priority(task_model.priority),
                    completed=task_model.completed,
                    due_date=task_model.due_date,
                    created_at=task_model.created_at
                )
                project.add_task(task)
        
        return project
