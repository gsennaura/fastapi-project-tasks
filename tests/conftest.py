"""Pytest configuration and shared fixtures."""

import asyncio
import pytest
import pytest_asyncio
import httpx
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient
from app.main import app
from app.infrastructure.database.models import Base
from app.dependencies import get_database
from app.infrastructure.config.settings import get_settings


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=False
)

TestSessionLocal = async_sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with overridden dependencies."""
    
    async def override_get_database():
        yield test_db
    
    app.dependency_overrides[get_database] = override_get_database
    
    # Add authentication header
    default_headers = {"Authorization": "Bearer dev-secret-key"}
    
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), 
        base_url="http://test",
        headers=default_headers
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_project_data():
    """Sample project data for tests."""
    return {
        "name": "Test Project",
        "description": "A test project for unit testing"
    }


@pytest.fixture
def sample_task_data():
    """Sample task data for tests."""
    return {
        "title": "Test Task",
        "description": "A test task",
        "priority": 5
    }
