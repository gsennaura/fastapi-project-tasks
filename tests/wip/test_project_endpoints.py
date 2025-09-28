"""Project endpoint tests."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities import Project
from app.domain.value_objects import ProjectId
from app.infrastructure.database.models import ProjectModel


class TestProjectEndpoints:

    
    @pytest.mark.asyncio
    async def test_create_project_success(self, client: AsyncClient):
        """Test successful project creation via API."""
        project_data = {
            "name": "Integration Test Project",
            "description": "Created via integration test"
        }
        
        response = await client.post("/projects/", json=project_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Integration Test Project"
        assert data["description"] == "Created via integration test"
        assert "id" in data
        assert "created_at" in data
    
    @pytest.mark.asyncio
    async def test_create_project_without_description(self, client: AsyncClient):
        """Test creating project without description."""
        project_data = {
            "name": "Project Without Description"
        }
        
        response = await client.post("/projects/", json=project_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Project Without Description"
        assert data["description"] is None
    
    @pytest.mark.asyncio
    async def test_create_project_invalid_data(self, client: AsyncClient):
        """Test creating project with invalid data."""
        project_data = {
            "name": ""  # Empty name should fail
        }
        
        response = await client.post("/projects/", json=project_data)
        
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_get_project_success(self, client: AsyncClient, test_db: AsyncSession):
        """Test getting existing project."""
        # Create project directly in database
        project_id = ProjectId.generate()
        db_project = ProjectModel(
            id=project_id.value,
            name="Test Project",
            description="Test description"
        )
        test_db.add(db_project)
        await test_db.commit()
        
        # Get project via API
        response = await client.get(f"/projects/{project_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Project"
        assert data["description"] == "Test description"
        assert data["id"] == str(project_id)
    
    @pytest.mark.asyncio
    async def test_get_project_not_found(self, client: AsyncClient):
        """Test getting non-existent project."""
        non_existent_id = ProjectId.generate()
        
        response = await client.get(f"/projects/{non_existent_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_update_project_success(self, client: AsyncClient, test_db: AsyncSession):
        """Test updating existing project."""
        # Create project
        project_id = ProjectId.generate()
        db_project = ProjectModel(
            id=project_id.value,
            name="Original Name",
            description="Original description"
        )
        test_db.add(db_project)
        await test_db.commit()
        
        # Update project
        update_data = {
            "name": "Updated Name",
            "description": "Updated description"
        }
        
        response = await client.put(f"/projects/{project_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"
    
    @pytest.mark.asyncio
    async def test_delete_project_success(self, client: AsyncClient, test_db: AsyncSession):
        """Test deleting existing project."""
        # Create project
        project_id = ProjectId.generate()
        db_project = ProjectModel(
            id=project_id.value,
            name="Project to Delete",
            description="Will be deleted"
        )
        test_db.add(db_project)
        await test_db.commit()
        
        # Delete project
        response = await client.delete(f"/projects/{project_id}")
        
        assert response.status_code == 204
    
    @pytest.mark.asyncio
    async def test_list_projects_empty(self, client: AsyncClient):
        """Test listing projects when none exist."""
        response = await client.get("/projects/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20
    
    @pytest.mark.asyncio
    async def test_list_projects_returns_data(self, client: AsyncClient, test_db: AsyncSession):
        """Test listing projects with existing data."""
        # Create multiple projects
        projects = []
        for i in range(3):
            project_id = ProjectId.generate()
            db_project = ProjectModel(
                id=project_id.value,
                name=f"Project {i+1}",
                description=f"Description {i+1}"
            )
            projects.append(db_project)
            test_db.add(db_project)
        
        await test_db.commit()
        
        # List projects
        response = await client.get("/projects/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["page_size"] == 20
    
    @pytest.mark.asyncio
    async def test_list_projects_pagination(self, client: AsyncClient, test_db: AsyncSession):
        """Test project listing with pagination."""
        # Create multiple projects
        for i in range(5):
            project_id = ProjectId.generate()
            db_project = ProjectModel(
                id=project_id.value,
                name=f"Project {i+1}",
                description=f"Description {i+1}"
            )
            test_db.add(db_project)
        
        await test_db.commit()
        
        # Test pagination
        response = await client.get("/projects?page=1&page_size=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2
