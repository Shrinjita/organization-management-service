class OrganizationManagementException(Exception):
    """Base exception for organization management service"""
    pass

class OrganizationNotFoundError(OrganizationManagementException):
    """Raised when organization is not found"""
    pass

class OrganizationAlreadyExistsError(OrganizationManagementException):
    """Raised when organization already exists"""
    pass

class AdminNotFoundError(OrganizationManagementException):
    """Raised when admin user is not found"""
    pass

class AdminAlreadyExistsError(OrganizationManagementException):
    """Raised when admin user already exists"""
    pass

class InvalidCredentialsError(OrganizationManagementException):
    """Raised when credentials are invalid"""
    pass

class UnauthorizedAccessError(OrganizationManagementException):
    """Raised when user tries to access unauthorized resource"""
    pass

class DatabaseError(OrganizationManagementException):
    """Raised for database-related errors"""
    pass

class ValidationError(OrganizationManagementException):
    """Raised for validation errors"""
    pass