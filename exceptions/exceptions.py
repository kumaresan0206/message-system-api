class NotFoundException(Exception):
    """Raised when a requested resource is not found."""
    def __init__(self, success=False, message="The requested resource was not found"):
        self.success = success
        self.message = message
        super().__init__(self.message)

class ValidationException(Exception):
    """Raised when validation of input data fails."""
    def __init__(self, success=False, message="Validation failed"):
        self.success = success
        self.message = message
        super().__init__(self.message)

class AuthenticationException(Exception):
    """Raised when authentication fails."""
    def __init__(self, success=False, message="Authentication failed"):
        self.success = success
        self.message = message
        
        super().__init__(self.message)

class UnauthorizedException(Exception):
    """Raised when a user is not authorized to perform an action."""
    def __init__(self, success=False, message="You are not authorized to perform this action"):
        self.success = success
        self.message = message
        super().__init__(self.message)

class ForbiddenException(Exception):
    """Raised when access to a resource is forbidden."""
    def __init__(self, success=False, message="Access to this resource is forbidden"):
        self.success = success
        self.message = message
        super().__init__(self.message)

class ConflictException(Exception):
    """Raised when a conflict occurs."""
    def __init__(self, success=False, message="A conflict occurred"):
        self.success = success
        self.message = message
        super().__init__(self.message)