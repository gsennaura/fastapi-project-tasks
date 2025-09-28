import uuid
from typing import Union


class ProjectId:
    """Value object for project identifier."""
    
    def __init__(self, value: Union[str, uuid.UUID]):
        if isinstance(value, str):
            try:
                self._value = uuid.UUID(value)
            except ValueError:
                raise ValueError(f"Invalid UUID format: {value}")
        elif isinstance(value, uuid.UUID):
            self._value = value
        else:
            raise TypeError("ProjectId must be initialized with str or UUID")
    
    @classmethod
    def generate(cls) -> "ProjectId":
        """Generate a new ProjectId."""
        return cls(uuid.uuid4())
    
    @property
    def value(self) -> uuid.UUID:
        return self._value
    
    def __str__(self) -> str:
        return str(self._value)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ProjectId):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
