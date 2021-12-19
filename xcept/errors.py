

class BaseError(Exception):

    def __init__(self, message):

        self.message = message

    def __str__(self):

        return self.message


class UsedPositionalArgumentError(BaseError):

    pass


class UnusedKeywordArgumentError(BaseError):

    def __init__(self, message, argument):

        super().__init__(message=message)
        self.argument = argument


class ArgsMatchingError(BaseError):

    def __init__(self, message, arg):

        super().__init__(message=message)
        self.arg = arg
