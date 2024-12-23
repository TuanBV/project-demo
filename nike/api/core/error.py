"""Exception raised for system errors."""
from helpers.const import CODE

class CommonException(Exception):
    """Exception raised for system errors.

    Attributes:
        code -- code which caused the error
        message -- explanation of the error
    """

    def __init__(self, code=CODE.API.ERROR, message="A system error has occurred"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.code} -> {self.message}"


class NoDataException(CommonException):
    """Exception raised for no data errors.

    Attributes:
        code -- code which caused the error
        message -- explanation of the error
    """

    def __init__(self, code=CODE.API.NO_CONTENT, message="No data found"):
        self.code = code
        self.message = message
        super().__init__(self.code, self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.code} -> {self.message}"


class UnauthorizedException(CommonException):
    """Exception raised for unauthorized errors.

    Attributes:
        code -- code which caused the error
        message -- explanation of the error
    """

    def __init__(self, code=CODE.API.INVALID_REQUEST, message="Authentication failed", cookie_config=None):
        self.code = code
        self.message = message
        self.cookie_config = cookie_config
        super().__init__(self.code, self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.code} -> {self.message}"


class PermissionException(CommonException):
    """Exception raised for permission errors.

    Attributes:
        code -- code which caused the error
        message -- explanation of the error
    """

    def __init__(self, code=CODE.API.INVALID_PERMISSION, message="You don't have permission"):
        self.code = code
        self.message = message
        super().__init__(self.code, self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.code} -> {self.message}"
