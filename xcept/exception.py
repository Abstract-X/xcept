from dataclasses import dataclass, field

from xcept.formatter import Formatter
from xcept import errors


_NON_FORMATTING_ATTRS = {"template_", "_formatter"}


@dataclass
class Exception_(Exception):
    ALLOW_UNUSED_ARGS = False
    template_: str = field(repr=False)

    def __post_init__(self):
        self._formatter = Formatter(allow_unused_args=self.ALLOW_UNUSED_ARGS)
        self._check_args_matching()

    def __str__(self):
        return self._get_message()

    def get_template(self) -> str:
        return self.template_

    def _get_formatting_attrs(self) -> dict:
        attrs = {}

        for key, value in vars(self).items():
            if key not in _NON_FORMATTING_ATTRS:
                attrs[key] = value

        return attrs

    def _get_message(self) -> str:
        return self._formatter.format(self.get_template(), **self._get_formatting_attrs())

    def _check_args_matching(self) -> None:
        try:
            self._get_message()
        except KeyError as error:
            arg = error.args[0]

            raise errors.ArgMatchingError(
                f"argument {arg!r} specified in template was not found among the attributes!",
                arg=arg
            ) from None
