class SelectelException(ValueError):
    pass


class InvalidSchema(SelectelException):
    pass


class EmptyUsername(SelectelException):
    pass


class EmptyPassword(SelectelException):
    pass


class EmptyContainerName(SelectelException):
    pass
