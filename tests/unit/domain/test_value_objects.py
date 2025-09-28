import pytest
import uuid
from app.domain.value_objects import ProjectId, TaskId, Priority


class TestProjectId:
    
    def test_create_from_uuid(self):
        """Create ProjectId from UUID."""
        test_uuid = uuid.uuid4()
        project_id = ProjectId(test_uuid)
        
        assert project_id.value == test_uuid
        assert str(project_id) == str(test_uuid)
    
    def test_create_from_string(self):
        """Create ProjectId from string."""
        test_uuid = uuid.uuid4()
        project_id = ProjectId(str(test_uuid))
        
        assert project_id.value == test_uuid
        assert str(project_id) == str(test_uuid)
    
    def test_invalid_string_raises_error(self):
        """Invalid string raises error."""
        with pytest.raises(ValueError, match="Invalid UUID format"):
            ProjectId("invalid-uuid")
    
    def test_invalid_type_raises_error(self):
        """Invalid type raises TypeError."""
        with pytest.raises(TypeError, match="ProjectId must be initialized with str or UUID"):
            ProjectId(123)
    
    def test_generate_new_project_id(self):
        """Test generating new ProjectId."""
        project_id = ProjectId.generate()
        
        assert isinstance(project_id, ProjectId)
        assert isinstance(project_id.value, uuid.UUID)
    
    def test_project_id_equality(self):
        """Test ProjectId equality."""
        test_uuid = uuid.uuid4()
        project_id1 = ProjectId(test_uuid)
        project_id2 = ProjectId(test_uuid)
        
        assert project_id1 == project_id2
    
    def test_project_id_inequality(self):
        """Test ProjectId inequality."""
        project_id1 = ProjectId.generate()
        project_id2 = ProjectId.generate()
        
        assert project_id1 != project_id2


class TestTaskId:
    
    def test_create_from_uuid(self):
        """Create TaskId from UUID."""
        test_uuid = uuid.uuid4()
        task_id = TaskId(test_uuid)
        
        assert task_id.value == test_uuid
        assert str(task_id) == str(test_uuid)
    
    def test_generate_new_task_id(self):
        """Test generating new TaskId."""
        task_id = TaskId.generate()
        
        assert isinstance(task_id, TaskId)
        assert isinstance(task_id.value, uuid.UUID)


class TestPriority:
    
    def test_create_valid_priority(self):
        """Create valid priority."""
        priority = Priority(5)
        assert priority.value == 5
    
    def test_create_priority_boundary_values(self):
        """Test creating priority with boundary values."""
        min_priority = Priority(1)
        max_priority = Priority(10)
        
        assert min_priority.value == 1
        assert max_priority.value == 10
    
    def test_create_priority_below_minimum_raises_error(self):
        """Test that priority below 1 raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be between 1 and 10"):
            Priority(0)
    
    def test_create_priority_above_maximum_raises_error(self):
        """Test that priority above 10 raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be between 1 and 10"):
            Priority(11)
    
    def test_priority_equality(self):
        """Test priority equality."""
        priority1 = Priority(5)
        priority2 = Priority(5)
        
        assert priority1 == priority2
    
    def test_priority_inequality(self):
        """Test priority inequality."""
        priority1 = Priority(5)
        priority2 = Priority(7)
        
        assert priority1 != priority2
    
    def test_priority_comparison(self):
        """Test priority comparison operations."""
        low_priority = Priority(3)
        high_priority = Priority(8)
        
        assert low_priority < high_priority
        assert high_priority > low_priority
        assert Priority(5) <= Priority(5)
        assert Priority(5) >= Priority(5)
