class Priority:
    """Value object for task priority."""
    
    MIN_PRIORITY = 1
    MAX_PRIORITY = 10
    DEFAULT_PRIORITY = 5
    
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Priority must be an integer")
        
        if not (self.MIN_PRIORITY <= value <= self.MAX_PRIORITY):
            raise ValueError(
                f"Priority must be between {self.MIN_PRIORITY} and {self.MAX_PRIORITY}"
            )
        
        self._value = value
    
    @property
    def value(self) -> int:
        return self._value
    
    def __str__(self) -> str:
        return str(self._value)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Priority):
            return False
        return self._value == other._value
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Priority):
            return NotImplemented
        return self._value < other._value
    
    def __le__(self, other) -> bool:
        if not isinstance(other, Priority):
            return NotImplemented
        return self._value <= other._value
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Priority):
            return NotImplemented
        return self._value > other._value
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, Priority):
            return NotImplemented
        return self._value >= other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
