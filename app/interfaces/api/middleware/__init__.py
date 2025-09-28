"""Authentication middleware."""

from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from ....infrastructure.config import get_settings


settings = get_settings()
security = HTTPBearer()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for API Key authentication."""
    
    PROTECTED_PATHS = [
        "/projects",
        "/tasks"
    ]
    
    async def dispatch(self, request: Request, call_next):
        """Process the request and check authentication."""
        
        # Skip authentication for docs and health endpoints
        if request.url.path in ["/", "/docs", "/redoc", "/openapi.json", "/health"]:
            response = await call_next(request)
            return response
        
        # Check if path requires authentication
        requires_auth = any(
            request.url.path.startswith(path) 
            for path in self.PROTECTED_PATHS
        )
        
        if requires_auth:
            api_key = self._extract_api_key(request)
            if not api_key or api_key != settings.api_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing API key",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        response = await call_next(request)
        return response
    
    def _extract_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from request headers."""
        # Try Authorization header first
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ", 1)[1]
        
        # Try X-API-Key header
        return request.headers.get("X-API-Key")
