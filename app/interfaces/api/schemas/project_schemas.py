"""Project API schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    """Schema for project creation request."""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class UpdateProjectRequest(BaseModel):
    """Schema for project update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: str = Field(..., description="Unique project ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    created_at: datetime = Field(..., description="Creation date")
    
    class Config:
        from_attributes = True
