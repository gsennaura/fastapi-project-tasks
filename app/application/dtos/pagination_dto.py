"""Pagination DTO."""

from typing import Optional
from pydantic import BaseModel, Field


class PaginationDTO(BaseModel):
    """DTO for pagination."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Page size")
    
    @property
    def offset(self) -> int:
        """Calculates offset based on page and size."""
        return (self.page - 1) * self.page_size
    
    @property 
    def limit(self) -> int:
        """Returns the limit (page_size)."""
        return self.page_size
