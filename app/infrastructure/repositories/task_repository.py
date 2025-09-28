"""Task repository with SQLAlchemy."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from ...domain.entities import Task
from ...domain.interfaces import TaskRepositoryInterface
from ...domain.value_objects import TaskId, ProjectId, Priority
from ...domain.exceptions import TaskNotFoundError
from ..database.models import TaskModel


class TaskRepository(TaskRepositoryInterface):
    """Task repository using SQLAlchemy."""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def create(self, task: Task) -> Task:
        """Creates a new task."""
        db_task = TaskModel(
            id=task.id.value,
            project_id=task.project_id.value,
            title=task.title,
            priority=task.priority.value,
            completed=task.completed,
            due_date=task.due_date,
            created_at=task.created_at
        )
        
        self._session.add(db_task)
        await self._session.commit()
        await self._session.refresh(db_task)
        
        return self._model_to_entity(db_task)
    
    async def get_by_id(self, task_id: TaskId) -> Optional[Task]:
        """Gets task by ID."""
        stmt = (
            select(TaskModel)
            .options(selectinload(TaskModel.project))
            .where(TaskModel.id == task_id.value)
        )
        result = await self._session.execute(stmt)
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            return None
        
        return self._model_to_entity(db_task)
    
    async def update(self, task: Task) -> Task:
        """Updates an existing task."""
        stmt = select(TaskModel).where(TaskModel.id == task.id.value)
        result = await self._session.execute(stmt)
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            raise TaskNotFoundError(str(task.id))
        
        db_task.title = task.title
        db_task.priority = task.priority.value
        db_task.completed = task.completed
        db_task.due_date = task.due_date
        
        await self._session.commit()
        await self._session.refresh(db_task)
        
        return self._model_to_entity(db_task)
    
    async def delete(self, task_id: TaskId) -> None:
        """Removes a task."""
        stmt = select(TaskModel).where(TaskModel.id == task_id.value)
        result = await self._session.execute(stmt)
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            raise TaskNotFoundError(str(task_id))
        
        await self._session.delete(db_task)
        await self._session.commit()
    
    async def get_by_project_id(
        self, 
        project_id: ProjectId, 
        limit: Optional[int] = None, 
        offset: int = 0
    ) -> List[Task]:
        """Lists tasks from a project ordered by priority (descending)."""
        stmt = (
            select(TaskModel)
            .where(TaskModel.project_id == project_id.value)
            .order_by(desc(TaskModel.priority), TaskModel.created_at)
            .offset(offset)
        )
        
        if limit:
            stmt = stmt.limit(limit)
        
        result = await self._session.execute(stmt)
        db_tasks = result.scalars().all()
        
        return [self._model_to_entity(db_task) for db_task in db_tasks]
    
    async def exists(self, task_id: TaskId) -> bool:
        """Checks if a task exists."""
        stmt = select(TaskModel.id).where(TaskModel.id == task_id.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def _model_to_entity(self, db_task: TaskModel) -> Task:
        """Converts SQLAlchemy model to domain entity."""
        return Task(
            id=TaskId(db_task.id),
            project_id=ProjectId(db_task.project_id),
            title=db_task.title,
            priority=Priority(db_task.priority),
            completed=db_task.completed,
            due_date=db_task.due_date,
            created_at=db_task.created_at
        )
