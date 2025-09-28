"""SQLAlchemy models."""

import uuid
from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class ProjectModel(Base):
    """SQLAlchemy model for Project."""
    
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    tasks = relationship("TaskModel", back_populates="project", cascade="all, delete-orphan")


class TaskModel(Base):
    """SQLAlchemy model for Task."""
    
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    priority = Column(Integer, nullable=False, default=5, index=True)
    completed = Column(Boolean, nullable=False, default=False, index=True)
    due_date = Column(Date, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    project = relationship("ProjectModel", back_populates="tasks")
