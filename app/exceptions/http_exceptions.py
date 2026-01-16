from fastapi import status

class BaseCustomError(Exception):
    """Base class for all custom exceptions"""
    def __init__(self, detail: str, status_code: int, error_code: str = None):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)

class BadRequestError(BaseCustomError):
    """Exception raised for invalid requests"""
    def __init__(self, detail: str = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)


class UnauthorizedError(BaseCustomError):
    """Exception raised for authentication failures"""
    def __init__(self, detail: str = "Unauthorized", headers: dict = None, error_code: str = "UNAUTHORIZED"):
        self.headers = headers or {}
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, error_code=error_code)

class InvalidJwtToken(BaseCustomError):
    def __init__(self,  detail: str= "Invalid jwt token", error_code: str= "INVALID TOKEN"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, error_code=error_code)

class InvalidNodeName(BaseCustomError):
    def __init__(self,  detail: str= "Invalid Folder Name", error_code: str= "Invalid Folder Name"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class NotaDirectory(BaseCustomError):
    def __init__(self,  detail: str= "Node is not a Directory", error_code: str= "Node is not a Directory"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class DirHasChild(BaseCustomError):
    def __init__(self,  detail: str= "Directory is not empty", error_code: str= "NON_EMPTY_DIR"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class NodeNotExsits(BaseCustomError):
    def __init__(self,  detail: str= "Node doesn't exsist", error_code: str= "NODE_NOT_EXSITS"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class NotaOwner(BaseCustomError):
    def __init__(self,  detail: str= "User is not owner of a node", error_code: str= "NOT_OWNER"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)

class PermissionDenied(BaseCustomError):
    def __init__(self,  detail: str= "Permission denied for the user", error_code: str= "PERMISSION_DENIED"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, error_code=error_code)