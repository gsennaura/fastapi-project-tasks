"""FastAPI main application."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from .infrastructure.config import get_settings
from .domain.exceptions import DomainException
from .exception_handlers import (
    domain_exception_handler,
    http_exception_handler, 
    validation_exception_handler,
    general_exception_handler
)
from .interfaces.api.middleware import AuthenticationMiddleware
from .interfaces.api.routers import projects, tasks


# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A scalable FastAPI backend service for managing Projects and Tasks",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthenticationMiddleware)

# Add exception handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/", tags=["health"])
async def root():
    """Root endpoint."""
    return {
        "message": "FastAPI Project Tasks API",
        "version": settings.app_version,
        "status": "healthy"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
