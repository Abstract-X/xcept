import string

from xcept import errors


class Formatter(string.Formatter):
    """Formatter for generating exception messages."""

    def __init__(self, allow_unused_args: bool):

        super().__init__()
        self._allow_unused_args = allow_unused_args

    def parse(self, format_string):

        for literal_text, field_name, format_spec, conversion in super().parse(format_string=format_string):
            if (field_name and (field_name in string.digits)) or (field_name == ""):
                raise errors.UsedPositionalArgumentError(f"positional argument is used!") from None
        iterator = super().parse(format_string=format_string)

        return iterator

    def check_unused_args(self, used_args, args, kwargs) -> None:

        if not self._allow_unused_args:
            for kwarg in kwargs:
                if kwarg not in used_args:
                    raise errors.UnusedKeywordArgumentError(
                        f"keyword argument {kwarg!r} is not used!", argument=kwarg
                    ) from None
