"""Base domain exception."""


class DomainException(Exception):
    """Base exception for domain-related errors."""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
