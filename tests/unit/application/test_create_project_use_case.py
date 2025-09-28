"""Use case tests."""

import pytest
from unittest.mock import AsyncMock, Mock
from app.application.use_cases import CreateProjectUseCase
from app.application.dtos import CreateProjectDTO
from app.domain.entities import Project
from app.domain.value_objects import ProjectId
from app.domain.interfaces import ProjectRepositoryInterface


class TestCreateProjectUseCase:

    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository."""
        return AsyncMock(spec=ProjectRepositoryInterface)
    
    @pytest.fixture
    def use_case(self, mock_repository):
        """Create use case with mock repository."""
        return CreateProjectUseCase(mock_repository)
    
    @pytest.mark.asyncio
    async def test_create_project_success(self, use_case, mock_repository):
        """Test successful project creation."""
        # Arrange
        dto = CreateProjectDTO(
            name="Test Project",
            description="Test description"
        )
        
        created_project = Project(
            id=ProjectId.generate(),
            name="Test Project",
            description="Test description"
        )
        
        mock_repository.create.return_value = created_project
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result.name == "Test Project"
        assert result.description == "Test description"
        assert result.id is not None
        mock_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_project_without_description(self, use_case, mock_repository):
        """Test creating project without description."""
        # Arrange
        dto = CreateProjectDTO(name="Test Project")
        
        created_project = Project(
            id=ProjectId.generate(),
            name="Test Project",
            description=None
        )
        
        mock_repository.create.return_value = created_project
        
        # Act
        result = await use_case.execute(dto)
        
        # Assert
        assert result.name == "Test Project"
        assert result.description is None
        mock_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_repository_called_with_correct_data(self, use_case, mock_repository):
        """Test that repository is called with correct project data."""
        # Arrange
        dto = CreateProjectDTO(
            name="Test Project",
            description="Test description"
        )
        
        created_project = Project(
            id=ProjectId.generate(),
            name="Test Project",
            description="Test description"
        )
        
        mock_repository.create.return_value = created_project
        
        # Act
        await use_case.execute(dto)
        
        # Assert
        mock_repository.create.assert_called_once()
        call_args = mock_repository.create.call_args[0][0]  # First positional argument
        
        assert isinstance(call_args, Project)
        assert call_args.name == "Test Project"
        assert call_args.description == "Test description"
        assert call_args.id is not None
