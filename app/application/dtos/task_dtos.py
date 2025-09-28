"""Task-related DTOs."""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class CreateTaskDTO(BaseModel):
    """DTO for task creation."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    priority: int = Field(5, ge=1, le=10, description="Task priority (1-10)")
    due_date: Optional[date] = Field(None, description="Due date")
    
    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v


class UpdateTaskDTO(BaseModel):
    """DTO for task update."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    priority: Optional[int] = Field(None, ge=1, le=10, description="Task priority (1-10)")
    completed: Optional[bool] = Field(None, description="Completion status")
    due_date: Optional[date] = Field(None, description="Due date")
    
    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskResponseDTO(BaseModel):
    """DTO for task response."""
    id: str = Field(..., description="Unique task ID")
    project_id: str = Field(..., description="Project ID")
    title: str = Field(..., description="Task title")
    priority: int = Field(..., description="Task priority")
    completed: bool = Field(..., description="Completion status")
    due_date: Optional[date] = Field(None, description="Due date")
    created_at: datetime = Field(..., description="Creation date")
    
    class Config:
        from_attributes = True
