import pytest
import httpx
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health endpoint works."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio 
async def test_openapi_schema():
    """Test API schema endpoint."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
