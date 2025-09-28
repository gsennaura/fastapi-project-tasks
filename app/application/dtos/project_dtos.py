"""Project-related DTOs."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateProjectDTO(BaseModel):
    """DTO for project creation."""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class UpdateProjectDTO(BaseModel):
    """DTO for project update."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectResponseDTO(BaseModel):
    """DTO for project response."""
    id: str = Field(..., description="Unique project ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    created_at: datetime = Field(..., description="Creation date")
    
    class Config:
        from_attributes = True
