from fastapi import HTTPException


class AlreadyExistsError(Exception):
    """Exception raised when trying to create a resource that already exists."""
    pass


class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""
    pass


class ValidationError(Exception):
    """Exception raised when input data fails validation."""
    pass


class AuthenticationError(HTTPException):
    """Exception raised when authentication fails."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)


class AuthorizationError(HTTPException):
    """Exception raised when authorization fails."""

    def __init__(self, detail: str = "Authorization failed"):
        super().__init__(status_code=403, detail=detail)


class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    pass
