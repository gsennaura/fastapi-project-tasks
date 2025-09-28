"""Application settings."""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # Security
    api_key: str = Field(..., env="API_KEY")
    
    # Pagination
    pagination_max_page_size: int = Field(100, env="PAGINATION_MAX_PAGE_SIZE")
    
    # App Info
    app_name: str = "FastAPI Project Tasks"
    app_version: str = "1.0.0"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Returns singleton instance of settings."""
    return Settings()
