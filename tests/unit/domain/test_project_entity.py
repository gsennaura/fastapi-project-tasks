import pytest
from datetime import datetime
from app.domain.entities import Project
from app.domain.value_objects import ProjectId
from app.domain.exceptions import ProjectValidationError


class TestProject:
    
    def test_create_project_valid_data(self):
        """Create project with valid data."""
        project_id = ProjectId.generate()
        project = Project(
            id=project_id,
            name="Test Project",
            description="Test description"
        )
        
        assert project.id == project_id
        assert project.name == "Test Project"
        assert project.description == "Test description"
        assert isinstance(project.created_at, datetime)
    
    def test_create_project_no_description(self):
        """Create project without description."""
        project_id = ProjectId.generate()
        project = Project(
            id=project_id,
            name="Test Project"
        )
        
        assert project.id == project_id
        assert project.name == "Test Project"
        assert project.description is None
    
    def test_empty_name_raises_error(self):
        """Empty name should raise error."""
        project_id = ProjectId.generate()
        
        with pytest.raises(ProjectValidationError):
            Project(
                id=project_id,
                name="",
                description="Test description"
            )
    
    def test_whitespace_name_raises_error(self):
        """Whitespace name should raise error."""
        project_id = ProjectId.generate()
        
        with pytest.raises(ProjectValidationError):
            Project(
                id=project_id,
                name="   ",
                description="Test description"
            )
    
    def test_update_project_name(self):
        """Test updating project name."""
        project_id = ProjectId.generate()
        project = Project(
            id=project_id,
            name="Original Name",
            description="Test description"
        )
        
        project.update_name("Updated Name")
        assert project.name == "Updated Name"
    
    def test_update_project_description(self):
        """Test updating project description."""
        project_id = ProjectId.generate()
        project = Project(
            id=project_id,
            name="Test Project",
            description="Original description"
        )
        
        project.update_description("Updated description")
        assert project.description == "Updated description"
    
    def test_project_equality(self):
        """Test project equality based on ID."""
        project_id = ProjectId.generate()
        
        project1 = Project(
            id=project_id,
            name="Project 1",
            description="Description 1"
        )
        
        project2 = Project(
            id=project_id,
            name="Project 2",
            description="Description 2"
        )
        
        assert project1 == project2  # Same ID, different data
    
    def test_project_inequality(self):
        """Test project inequality with different IDs."""
        project1 = Project(
            id=ProjectId.generate(),
            name="Project 1",
            description="Description 1"
        )
        
        project2 = Project(
            id=ProjectId.generate(),
            name="Project 1",
            description="Description 1"
        )
        
        assert project1 != project2  # Different IDs, same data
