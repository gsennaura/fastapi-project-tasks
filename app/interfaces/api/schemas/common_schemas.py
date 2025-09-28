"""Common API schemas."""

from typing import Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class MessageResponse(BaseModel):
    """Schema for simple messages."""
    message: str
