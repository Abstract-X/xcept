from typing import Any


class BaseError(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class UsedPositionalArgError(BaseError):
    pass


class UnusedKeywordArgError(BaseError):

    def __init__(self, message: str, arg: str):
        super().__init__(message=message)
        self.arg = arg


class ArgMatchingError(BaseError):

    def __init__(self, message: str, arg: Any):
        super().__init__(message=message)
        self.arg = arg
